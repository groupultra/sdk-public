.. _moobius_network_ws_client:

###################################################################################
moobius.network.ws_client
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.ws_client.asserted_dataclass_asdict:

asserted_dataclass_asdict
---------------------------------------------------------------------------------------------------------------------



Asserts that the input is the correct dataclass or is a dict which matches to a dataclsss.

.. raw:: html

  <embed>
  <head>
    <style>
        .style846 {
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
    <p class="style846">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **asserted_dataclass_asdict**(x, the_class)

.. raw:: html

  <embed>
  <head>
    <style>
        .style847 {
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
    <p class="style847">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **x:** The input dict or dataclass.

* **the_class:** The class to match to, such as types.Button.

.. raw:: html

  <embed>
  <head>
    <style>
        .style848 {
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
    <p class="style848">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The modified value of x, as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style849 {
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
    <p class="style849">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception if there is a mismatch in the formatting.



.. _moobius.network.ws_client.time_out_wrap:

time_out_wrap
---------------------------------------------------------------------------------------------------------------------



Sometimes the connection can hang forever. Adds a timeout that will make await raise an asyncio.TimeoutError if the function takes too long..

.. raw:: html

  <embed>
  <head>
    <style>
        .style850 {
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
    <p class="style850">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **time_out_wrap**(co_routine, timeout)

.. raw:: html

  <embed>
  <head>
    <style>
        .style851 {
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
    <p class="style851">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **co_routine:** Co-routine.

* **timeout=16:** A timeout.

.. raw:: html

  <embed>
  <head>
    <style>
        .style852 {
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
    <p class="style852">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The co-routine with a timeout.

.. raw:: html

  <embed>
  <head>
    <style>
        .style853 {
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
    <p class="style853">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



************************************
Class WSClient
************************************

WSClient is a websocket client that has a wide variety of Moobius-specific functions for sending payloads specific to the Moobius platform.
It contains the standard socket functions such as on_connect(), send(), and receive() and is more robust:
it has a queuing system and will automatically reconnect.

.. _moobius.network.ws_client.WSClient.connect:

WSClient.connect
---------------------------------------------------------------------------------------------------------------------



Connects to the websocket server. Call after self.authenticate(). 
Keeps trying if it fails!.

.. raw:: html

  <embed>
  <head>
    <style>
        .style854 {
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
    <p class="style854">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.connect**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style855 {
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
    <p class="style855">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style856 {
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
    <p class="style856">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style857 {
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
    <p class="style857">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send:

WSClient.send
---------------------------------------------------------------------------------------------------------------------



Adds the message to self.outbound_queue for sending to the server.
Note: Call this and other socket functions after self.authenticate()
 If the server responds to the message it will be detected in the self.recieve() loop.

.. raw:: html

  <embed>
  <head>
    <style>
        .style858 {
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
    <p class="style858">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send**(self, message)

.. raw:: html

  <embed>
  <head>
    <style>
        .style859 {
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
    <p class="style859">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **message:** Dict-valued message (or JSON string).

.. raw:: html

  <embed>
  <head>
    <style>
        .style860 {
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
    <p class="style860">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style861 {
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
    <p class="style861">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.receive:

WSClient.receive
---------------------------------------------------------------------------------------------------------------------



Waits in a loop for messages from the websocket server or from the wand queue. Never.

.. raw:: html

  <embed>
  <head>
    <style>
        .style862 {
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
    <p class="style862">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.receive**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style863 {
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
    <p class="style863">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style864 {
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
    <p class="style864">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The 
Reconnectes if the connection fails or self.websocket.recv() stops getting anything (no heartbeats nor messages).

.. raw:: html

  <embed>
  <head>
    <style>
        .style865 {
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
    <p class="style865">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.safe_handle:

WSClient.safe_handle
---------------------------------------------------------------------------------------------------------------------



Handles it with self.handle, which is specified on construction, catching errors.

.. raw:: html

  <embed>
  <head>
    <style>
        .style866 {
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
    <p class="style866">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.safe_handle**(self, message)

.. raw:: html

  <embed>
  <head>
    <style>
        .style867 {
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
    <p class="style867">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **message:** String-valued message from the websocket server.

.. raw:: html

  <embed>
  <head>
    <style>
        .style868 {
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
    <p class="style868">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style869 {
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
    <p class="style869">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.heartbeat:

WSClient.heartbeat
---------------------------------------------------------------------------------------------------------------------



Sends a heartbeat..

.. raw:: html

  <embed>
  <head>
    <style>
        .style870 {
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
    <p class="style870">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.heartbeat**(self, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style871 {
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
    <p class="style871">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **dry_run:** N optional dry_run to not send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style872 {
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
    <p class="style872">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style873 {
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
    <p class="style873">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.dumps:

WSClient.dumps
---------------------------------------------------------------------------------------------------------------------



A slightly better json.dumps..

.. raw:: html

  <embed>
  <head>
    <style>
        .style874 {
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
    <p class="style874">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.dumps**(data)

.. raw:: html

  <embed>
  <head>
    <style>
        .style875 {
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
    <p class="style875">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **data:** Datastructure or dataclass and.

.. raw:: html

  <embed>
  <head>
    <style>
        .style876 {
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
    <p class="style876">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  JSON string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style877 {
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
    <p class="style877">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.service_login:

WSClient.service_login
---------------------------------------------------------------------------------------------------------------------



Logs in. Much like the HTTP api, this needs to be sent before any other messages.

.. raw:: html

  <embed>
  <head>
    <style>
        .style878 {
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
    <p class="style878">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.service_login**(self, service_id, access_token, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style879 {
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
    <p class="style879">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** The client_id of a Moobius service object, which is the ID of the running service.
    Used in almost every function.

* **access_token:** TODO; This is the access token from http_api_wrapper; for clean code decouple access_token here!.

* **dry_run:** Don't acually send anything (must functions offer a dry-run option).

.. raw:: html

  <embed>
  <head>
    <style>
        .style880 {
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
    <p class="style880">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style881 {
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
    <p class="style881">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.user_login:

WSClient.user_login
---------------------------------------------------------------------------------------------------------------------



Logs-in a user.
Every 2h AWS will force-disconnect, so it is a good idea to send this on connect.

.. raw:: html

  <embed>
  <head>
    <style>
        .style882 {
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
    <p class="style882">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.user_login**(self, access_token, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style883 {
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
    <p class="style883">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **access_token:** Used in the user_login message that is sent.
    This is the access token from http_api_wrapper.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style884 {
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
    <p class="style884">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style885 {
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
    <p class="style885">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.leave_channel:

WSClient.leave_channel
---------------------------------------------------------------------------------------------------------------------



A user leaves the channel with channel_id, unless dry_run is True..

.. raw:: html

  <embed>
  <head>
    <style>
        .style886 {
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
    <p class="style886">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.leave_channel**(self, user_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style887 {
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
    <p class="style887">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** User_id.

* **channel_id:** The channel_id.

* **dry_run:** Whether to dry_run.

.. raw:: html

  <embed>
  <head>
    <style>
        .style888 {
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
    <p class="style888">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent.

.. raw:: html

  <embed>
  <head>
    <style>
        .style889 {
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
    <p class="style889">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.join_channel:

WSClient.join_channel
---------------------------------------------------------------------------------------------------------------------



A user joins the channel with channel_id, unless dry_run is True..

.. raw:: html

  <embed>
  <head>
    <style>
        .style890 {
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
    <p class="style890">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.join_channel**(self, user_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style891 {
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
    <p class="style891">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** User_id.

* **channel_id:** The channel_id.

* **dry_run:** Whether to dry_run.

.. raw:: html

  <embed>
  <head>
    <style>
        .style892 {
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
    <p class="style892">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent.

.. raw:: html

  <embed>
  <head>
    <style>
        .style893 {
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
    <p class="style893">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_characters:

WSClient.send_characters
---------------------------------------------------------------------------------------------------------------------



Updates the characters that the recipients see.

.. raw:: html

  <embed>
  <head>
    <style>
        .style894 {
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
    <p class="style894">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_characters**(self, characters, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style895 {
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
    <p class="style895">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **characters:** The group id to represent the characters who are updated.

* **service_id:** As always.

* **channel_id:** The channel id.

* **recipients:** The group id to send to.

* **dry_run:** If True don't acually send the message (messages are sent in thier JSON-strin format).

.. raw:: html

  <embed>
  <head>
    <style>
        .style896 {
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
    <p class="style896">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style897 {
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
    <p class="style897">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_buttons:

WSClient.send_buttons
---------------------------------------------------------------------------------------------------------------------



Updates the buttons that the recipients see.

.. raw:: html

  <embed>
  <head>
    <style>
        .style898 {
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
    <p class="style898">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_buttons**(self, buttons, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style899 {
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
    <p class="style899">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **buttons:** The buttons list to be updated.

* **service_id:** As always.

* **channel_id:** The channel id.

* **recipients:** The group id to send to.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style900 {
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
    <p class="style900">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style901 {
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
    <p class="style901">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style902 {
            background-color: #DDBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style902">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> continue_button =
      >>>   {"button_name": "Continue Playing", "button_id": "play",
      >>>    "button_name": "Continue Playing", "new_window": False,
      >>>    "arguments": []}
      >>> ws_client.update_buttons("service_id", "channel_id", [continue_button], ["user1", "user2"])



.. _moobius.network.ws_client.WSClient.send_menu:

WSClient.send_menu
---------------------------------------------------------------------------------------------------------------------



Updates the right-click menu that the recipients can open on various messages.

.. raw:: html

  <embed>
  <head>
    <style>
        .style903 {
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
    <p class="style903">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_menu**(self, menu_items, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style904 {
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
    <p class="style904">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **menu_items:** List of MenuItem dataclasses.

* **service_id:** As always.

* **channel_id:** The channel id.

* **recipients:** The group id to send the changes to.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style905 {
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
    <p class="style905">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style906 {
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
    <p class="style906">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_style:

WSClient.send_style
---------------------------------------------------------------------------------------------------------------------



Updates the style (whether the canvas is expanded, other look-and-feel aspects) that the recipients see.

.. raw:: html

  <embed>
  <head>
    <style>
        .style907 {
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
    <p class="style907">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_style**(self, style_items, service_id, channel_id, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style908 {
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
    <p class="style908">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **style_items:** The style content to be updated. Dicts are converted into 1-elemnt lists.

* **service_id:** As always.

* **channel_id:** The channel id.

* **recipients:** The group id to send to.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style909 {
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
    <p class="style909">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style910 {
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
    <p class="style910">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style911 {
            background-color: #DDBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style911">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> style_items = [
        >>>   {
        >>>     "widget": "channel",
        >>>     "display": "invisible",
        >>>   },
        >>>   {
        >>>     "widget": "button",
        >>>     "display": "highlight",
        >>>     "button_hook": {
        >>>       "button_id": "button_id",
        >>>       "button_name": "done",
        >>>       "arguments": []
        >>>       },
        >>>     "text": "<h1>Start from here.</h1><p>This is a Button, which most channels have</p>"
        >>>   }]
        >>> ws_client.update_style("service_id", "channel_id", style_items, ["user1", "user2"])



.. _moobius.network.ws_client.WSClient.update_channel_info:

WSClient.update_channel_info
---------------------------------------------------------------------------------------------------------------------



Updates the channel name, description, etc for a given channel.

.. raw:: html

  <embed>
  <head>
    <style>
        .style912 {
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
    <p class="style912">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.update_channel_info**(self, channel_info, service_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style913 {
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
    <p class="style913">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_info:** The data of the update.

* **service_id:** As always.

* **channel_id:** The channel id.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style914 {
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
    <p class="style914">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style915 {
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
    <p class="style915">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style916 {
            background-color: #DDBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style916">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> ws_client.update_channel_info("service_id", "channel_id", {"name": "new_channel_name"})



.. _moobius.network.ws_client.WSClient.update_canvas:

WSClient.update_canvas
---------------------------------------------------------------------------------------------------------------------



Updates the canvas that the recipients see.

.. raw:: html

  <embed>
  <head>
    <style>
        .style917 {
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
    <p class="style917">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.update_canvas**(self, service_id, channel_id, canvas_items, recipients, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style918 {
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
    <p class="style918">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** As always.

* **channel_id:** The channel id.

* **canvas_items:** The elements to push to the canvas.

* **recipients:** The recipients character_ids who see the update.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style919 {
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
    <p class="style919">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style920 {
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
    <p class="style920">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)


.. raw:: html

  <embed>
  <head>
    <style>
        .style921 {
            background-color: #DDBBDD;
            padding: 5px;
            border-radius: 2px;
            font-family: Times New Roman;
            color: black;
            font-size: 16px;
        }
    </style>
  </head>
  <body>
    <p class="style921">
          <b>Example:</b>
    </p>
  </body>
  </embed>

    >>> canvas1 = CanvasItem(path="image/url", text="the_text")
      >>> canvas2 = CanvasItem(text="the_text2")
      >>> ws_client.update_canvas("service_id", "channel_id", [canvas1, canvas2], ["user1", "user2"])



.. _moobius.network.ws_client.WSClient.update:

WSClient.update
---------------------------------------------------------------------------------------------------------------------



A generic update function that is rarely used.

.. raw:: html

  <embed>
  <head>
    <style>
        .style922 {
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
    <p class="style922">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.update**(self, data, target_client_id, service_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style923 {
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
    <p class="style923">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **data:** The content of the update.

* **target_client_id:** The target client id (TODO: not currently used).

* **service_id:** The ID of the service.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style924 {
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
    <p class="style924">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style925 {
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
    <p class="style925">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.message_up:

WSClient.message_up
---------------------------------------------------------------------------------------------------------------------



Used by users to send messages.

.. raw:: html

  <embed>
  <head>
    <style>
        .style926 {
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
    <p class="style926">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.message_up**(self, user_id, service_id, channel_id, recipients, subtype, content, context, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style927 {
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
    <p class="style927">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** An enduser id generally.

* **service_id:** Which service to send to.

* **channel_id:** Which channel to broadcast the message in.

* **recipients:** The group id to send to.

* **subtype:** The subtype of message to send (text, etc). Goes into message['body'] JSON.

* **content:** What is inside the message['body']['content'] JSON.

* **context:** Optional metadata.

* **dry_run=None:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style928 {
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
    <p class="style928">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style929 {
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
    <p class="style929">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.message_down:

WSClient.message_down
---------------------------------------------------------------------------------------------------------------------



Sends a message to the recipients.

.. raw:: html

  <embed>
  <head>
    <style>
        .style930 {
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
    <p class="style930">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.message_down**(self, user_id, service_id, channel_id, recipients, subtype, content, sender, context, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style931 {
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
    <p class="style931">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** An service id generally.

* **service_id:** Which service to send to.

* **channel_id:** Which channel to broadcast the message in.

* **recipients:** The group id to send to.

* **subtype:** The subtype of message to send (text, etc). Goes into message['body'] JSON.

* **content:** What is inside the message['body']['content'] JSON.

* **sender:** The sender ID of the message, which determines who the chat shows the message as sent by.

* **context:** Optional metadata.

* **dry_run=None:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style932 {
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
    <p class="style932">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style933 {
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
    <p class="style933">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_button_click:

WSClient.send_button_click
---------------------------------------------------------------------------------------------------------------------



Sends a button click as a user.

.. raw:: html

  <embed>
  <head>
    <style>
        .style934 {
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
    <p class="style934">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_button_click**(self, button_id, bottom_button_id, button_args, channel_id, user_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style935 {
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
    <p class="style935">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **button_id:** The button's ID.

* **bottom_button_id:** The bottom button, set to "confirm" if there is no bottom button.

* **button_args:** What arguments (if any) were selected on the button (use an empty list of there are none).

* **channel_id:** The id of the channel the user pressed the button in.

* **user_id:** The ID of the (user mode) service.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style936 {
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
    <p class="style936">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style937 {
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
    <p class="style937">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.send_menu_item_click:

WSClient.send_menu_item_click
---------------------------------------------------------------------------------------------------------------------



Sends a menu item click as a user.

.. raw:: html

  <embed>
  <head>
    <style>
        .style938 {
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
    <p class="style938">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.send_menu_item_click**(self, menu_item_id, bottom_button_id, button_args, the_message, channel_id, user_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style939 {
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
    <p class="style939">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **menu_item_id:** The menu item's ID.

* **bottom_button_id:** The bottom button, set to "confirm" if there is no bottom button.

* **button_args:** What arguments (if any) were selected on the menu item's dialog (use an empty list of there are none).

* **the_message:** Can be a string-valued message_id, or a full message body. If a full message the subtype and content will be filled in.

* **channel_id:** The id of the channel the user pressed the button in.

* **user_id:** The ID of the (user mode) service.

* **dry_run:** Don't actually send anything if True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style940 {
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
    <p class="style940">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message sent as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style941 {
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
    <p class="style941">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.ws_client.WSClient.refresh_as_user:

WSClient.refresh_as_user
---------------------------------------------------------------------------------------------------------------------



Refreshes everything the user can see. The socket will send back messages with the information later.

.. raw:: html

  <embed>
  <head>
    <style>
        .style942 {
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
    <p class="style942">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **WSClient.refresh_as_user**(self, user_id, channel_id, dry_run)

.. raw:: html

  <embed>
  <head>
    <style>
        .style943 {
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
    <p class="style943">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** Used in the "action" message that is sent.

* **channel_id:** Used in the body of said message.

* **dry_run:** Don't actually send anything if True.
    These three parameters are common to most fetch messages.

.. raw:: html

  <embed>
  <head>
    <style>
        .style944 {
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
    <p class="style944">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The message that was sent as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style945 {
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
    <p class="style945">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.network.ws_client_internal_attrs <moobius.network.ws_client_internal_attrs>
