.. _moobius_core_groups:

###################################################################################
moobius.core.groups
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.core.groups.group2ids:

group2ids
---------------------------------------------------------------------------------------------------------------------

Converts a group id from the service into a list of character ids..

* Signature

    * group2ids(group_id, payload_body, http_api, client_id)

* Parameters

    * group_id: Group_id.
    
    * payload_body: The payload body.
    
    * http_api: The http_api client.
    
    * client_id: The client_id.

* Returns

  * The  list of character ids.

* Raises

  * (this function does not raise any notable errors)

************************************
Class ServiceGroupLib
************************************

(This class is for internal use).
Conversion between lists of member_ids and a group_id. The CCS app only ever sees a list of user ids.
Holds a library of groups, creating new groups if it gets a new set of users.
   The lookup is O(n) so performance at extremly large list sizes may require optimizations.

.. _moobius.core.groups.ServiceGroupLib.convert_list:

ServiceGroupLib.convert_list
---------------------------------------------------------------------------------------------------------------------

Converts a list to single group id, unless it is already a group id.

* Signature

    * ServiceGroupLib.convert_list(self, http_api, character_ids, is_message_down, channel_id)

* Parameters

    * http_api: The http_api client in Moobius.
    
    * character_ids: List of ids. If a string, treated as a one element list.
    
    * is_message_down: True = message_down (a message sent from the service), False = message_up (a message sent from a user).
    
    * channel_id=None: If None and the conversion still needs to happen it will raise an Exception.

* Returns

  * The group id.

* Raises

  * (this function does not raise any notable errors)

Class attributes
--------------------


