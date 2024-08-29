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
    <style>
        .style112 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style112">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **group2ids**(group_id, payload_body, http_api, client_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style113 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style113">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **group_id:** Group_id.

* **payload_body:** The payload body.

* **http_api:** The http_api client.

* **client_id:** The client_id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style114 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style114">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of character ids.

.. raw:: html

  <embed>
  <head>
    <style>
        .style115 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style115">
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
    <style>
        .style116 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style116">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **ServiceGroupLib.convert_list**(self, http_api, character_ids, is_message_down, channel_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style117 {
            background-color: #BBDDDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style117">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **http_api:** The http_api client in Moobius.

* **character_ids:** List of ids. If a string, treated as a one element list.

* **is_message_down:** True = message_down (a message sent from the service), False = message_up (a message sent from a user).

* **channel_id=None:** If None and the conversion still needs to happen it will raise an Exception.

.. raw:: html

  <embed>
  <head>
    <style>
        .style118 {
            background-color: #BBBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style118">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The group id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style119 {
            background-color: #DDBBBB;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style119">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------


