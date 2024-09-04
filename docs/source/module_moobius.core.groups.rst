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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **group2ids**(group_id, payload_body, http_api, client_id)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __group_id:__ Group_id.

* __payload_body:__ The payload body.

* __http_api:__ The http_api client.

* __client_id:__ The client_id.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of character ids.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

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

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **ServiceGroupLib.convert_list**(self, http_api, character_ids, is_message_down, channel_id)

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fparam">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* __http_api:__ The http_api client in Moobius.

* __character_ids:__ List of ids. If a string, treated as a one element list.

* __is_message_down:__ True = message_down (a message sent from the service), False = message_up (a message sent from a user).

* __channel_id=None:__ If None and the conversion still needs to happen it will raise an Exception.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="freturn">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The group id.

.. raw:: html

  <embed>
  <head>
  </head>
  <body>
    <p class="fraises">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------


