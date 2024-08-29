# Handles conversion between a group id and a list of user ids.
import os, asyncio

from loguru import logger

from moobius import types


class ServiceGroupLib():
    """
    (This class is for internal use).
    Conversion between lists of member_ids and a group_id. The CCS app only ever sees a list of user ids.
    Holds a library of groups, creating new groups if it gets a new set of users.
       The lookup is O(n) so performance at extremly large list sizes may require optimizations.
    """

    def __init__(self):
        """Creates an empty ServiceGroupLib instance."""
        logger.info(f'Initialized new, empty ServiceGroupLib on process {os.getpid()}')
        self.id2ids_mdown = {} # Message down creates service group with /service/group/create
        self.ids2id_mdown = {}
        self.id2ids_mup = {}
        self.ids2id_mup = {}
        self.alock = asyncio.Lock()

    async def convert_list(self, http_api, character_ids, is_message_down, channel_id=None):
        """
        Converts a list to single group id, unless it is already a group id.

        Parameters:
          http_api: The http_api client in Moobius
          character_ids: List of ids. If a string, treated as a one element list.
          is_message_down: True = message_down (a message sent from the service), False = message_up (a message sent from a user).
          channel_id=None: If None and the conversion still needs to happen it will raise an Exception.

        Returns: The group id.
        """
        if is_message_down:
            ids2id = self.id2ids_mdown
            id2ids = self.id2ids_mdown
        else:
            ids2id = self.id2ids_mup
            id2ids = self.id2ids_mup
        async with self.alock: # Make sure the old list is stored before the new list is created.
            character_ids = types.to_char_id_list(character_ids)
            if len(character_ids) == 0:
                return None
            else: # Convert list to a single group id in this mode.
                massive_str = '_'.join(character_ids)
                need_new_group = massive_str not in ids2id
                if need_new_group: # Call /service/group/create
                    character_ids = character_ids.copy()
                    if is_message_down:
                        group_id = (await http_api.create_service_group(character_ids)).group_id
                    else:
                        if not channel_id:
                            raise Exception('A channel_id must be specified when is_message_down is False')
                        group_id = (await http_api.create_channel_group(channel_id, 'A_message_up_group', character_ids)).group_id
                    ids2id[massive_str] = group_id
                    id2ids[group_id] = character_ids
                out = ids2id[massive_str]
                logger.info(f'Converted recipient list (is_mdown={is_message_down}) {character_ids} to group id {out} on process {os.getpid()}. {"Created new service group." if need_new_group else "Group already exists."}')
                return out


async def group2ids(group_id, payload_body, http_api, client_id):
    """Converts a group id from the service into a list of character ids. Accepts the group_id, the payload body, the http_api client, and the client_id. Returns a list of character ids."""
    if group_id==types.SERVICE:
        return []
    if type(group_id) is not str:
        raise Exception('Group id not a string.')

    channel_id = payload_body['channel_id']
    use_sgroup = False
    use_cgroup = True
    try:
        if use_sgroup:
            out_sgroup = await http_api.character_ids_of_service_group(group_id)
        else:
            out_sgroup = []
        sgroup_err = None
    except Exception as e:
        out_sgroup = []
        sgroup_err = e
    try:
        if use_cgroup:
            use_sender_when_possible = True
            the_id = client_id
            if 'sender' in payload_body and use_sender_when_possible:
                the_id = payload_body['sender']
            out_cgroup = await http_api.character_ids_of_channel_group(the_id, channel_id, group_id)
        else:
            out_cgroup = []
        cgroup_err = None
    except Exception as e:
        out_cgroup = []
        cgroup_err = e
    out = out_sgroup+out_cgroup
    logger.info(f'Extract character ids from group: {group_id} service_group {"error "+str(sgroup_err) if sgroup_err else "no error"}, channel_group {"error "+str(cgroup_err) if cgroup_err else "no error"}. Id list: {out}')
    if len(out)==0:
        logger.warning('Neither the channel nor service group queries were able to find any members in the group.')
    return out
