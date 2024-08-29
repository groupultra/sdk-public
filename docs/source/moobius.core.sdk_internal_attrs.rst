
####################
Private functions
####################

.. _moobius.core.sdk.Moobius._set_loguru:

Moobius._set_loguru
---------------------------------------------------------------------------------------------------------------------



Sets the log levels etc.  Set after setting self._config.

.. raw:: html

  <embed>
  <head>
    <style>
        .style435 {
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
    <p class="style435">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius._set_loguru**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style436 {
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
    <p class="style436">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style437 {
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
    <p class="style437">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style438 {
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
    <p class="style438">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.sdk.Moobius._convert_message_content:

Moobius._convert_message_content
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style439 {
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
    <p class="style439">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius._convert_message_content**(self, subtype, content)

.. raw:: html

  <embed>
  <head>
    <style>
        .style440 {
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
    <p class="style440">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **subtype:** Subtype.

* **content:** The string or dict-valued content,.

.. raw:: html

  <embed>
  <head>
    <style>
        .style441 {
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
    <p class="style441">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  MessageContent object.

.. raw:: html

  <embed>
  <head>
    <style>
        .style442 {
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
    <p class="style442">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.sdk.Moobius._update_rec:

Moobius._update_rec
---------------------------------------------------------------------------------------------------------------------



Use this function in the in the "recipients" fields of the websocket.
Converts lists into group_id strings, creating a group if need be, when.

.. raw:: html

  <embed>
  <head>
    <style>
        .style443 {
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
    <p class="style443">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius._update_rec**(self, recipients, is_m_down, channel_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style444 {
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
    <p class="style444">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **recipients:** Recipients.

* **is_m_down:** True if a message down.

* **channel_id=None:** The channel_id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style445 {
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
    <p class="style445">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The converted list.

.. raw:: html

  <embed>
  <head>
    <style>
        .style446 {
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
    <p class="style446">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.sdk.Moobius._checkin:

Moobius._checkin
---------------------------------------------------------------------------------------------------------------------



Called as a rate task, used to resync users, etc. Only called after on_start().

.. raw:: html

  <embed>
  <head>
    <style>
        .style447 {
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
    <p class="style447">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius._checkin**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style448 {
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
    <p class="style448">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style449 {
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
    <p class="style449">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style450 {
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
    <p class="style450">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.sdk.Moobius.__str__:

Moobius.__str__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

.. raw:: html

  <embed>
  <head>
    <style>
        .style451 {
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
    <p class="style451">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius.__str__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style452 {
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
    <p class="style452">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style453 {
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
    <p class="style453">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style454 {
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
    <p class="style454">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.sdk.Moobius.__repr__:

Moobius.__repr__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

.. raw:: html

  <embed>
  <head>
    <style>
        .style455 {
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
    <p class="style455">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius.__repr__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style456 {
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
    <p class="style456">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style457 {
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
    <p class="style457">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style458 {
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
    <p class="style458">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.core.sdk.Moobius.handle_received_payload._group2ids:

Moobius.handle_received_payload._group2ids
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style459 {
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
    <p class="style459">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **Moobius.handle_received_payload._group2ids**(g_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style460 {
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
    <p class="style460">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **g_id:** Gorup id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style461 {
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
    <p class="style461">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of character id strings.

.. raw:: html

  <embed>
  <head>
    <style>
        .style462 {
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
    <p class="style462">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



####################
Private attributes
####################

Moobius.handle_received_payload._group2ids 

Moobius.handle_received_payload._group2ids 
