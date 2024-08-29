.. _moobius_network_http_api_wrapper:

###################################################################################
moobius.network.http_api_wrapper
###################################################################################

******************************
Module-level functions
******************************

.. _moobius.network.http_api_wrapper.summarize_html:

summarize_html
---------------------------------------------------------------------------------------------------------------------



Creates a summary.
Converts HTML to an easier-for-a-human format by cutting out some of the more common tags. Far from perfect.

.. raw:: html

  <embed>
  <head>
    <style>
        .style654 {
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
    <p class="style654">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **summarize_html**(html_str)

.. raw:: html

  <embed>
  <head>
    <style>
        .style655 {
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
    <p class="style655">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **html_str:** N html_string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style656 {
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
    <p class="style656">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The summary as a string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style657 {
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
    <p class="style657">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.get_or_post:

get_or_post
---------------------------------------------------------------------------------------------------------------------



Sends a GET or POST request and awaits for the response.

.. raw:: html

  <embed>
  <head>
    <style>
        .style658 {
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
    <p class="style658">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **get_or_post**(url, is_post, requests_kwargs, raise_json_decode_errors)

.. raw:: html

  <embed>
  <head>
    <style>
        .style659 {
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
    <p class="style659">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **url:** Https://...

* **is_post:** False for GET, True for POST.

* **requests_kwargs=None:** These are fed into the requests/session get/post function.

* **raise_json_decode_errors=True:** Raise errors parsing the JSON that the request sends back, otherwise return the error as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style660 {
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
    <p class="style660">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  dict which is the json.loads() of the return.
  Error condition if JSON decoding fails:
    dict['code'] contains the code
      10000 is "good" (but the JSON still failed).
      204 indicates no return but without error which is also fine.
      Many other codes exist.
    dict['blob'] is the response text in cases where the JSON fail and raise_json is False.

.. raw:: html

  <embed>
  <head>
    <style>
        .style661 {
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
    <p class="style661">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception if Json fails and raise_json is True. Not all non-error returns are JSON thus the "blob" option.



************************************
Class BadResponseException
************************************

For when the network is not doing what it should.



Class attributes
--------------------

BadResponseException.Exception 

************************************
Class HTTPAPIWrapper
************************************

Helper class for interacting with the Moobius HTTP API.
All methods except for authenticate() and refresh() require authentication headers. 
When calling these methods, make sure to call authenticate() first and add headers=self.headers to the method call.

This wrapper's methods are categorized as follows:
  Auth: Authentication and sign in/out.
  User: Dealing with real users.
  Service: Apps use this API to be a service.
  Channel: Dealing with threads/channels/chat-rooms etc.
  File: Upload files (automatically fetches the URL needed).
  Group: Combine users, services, or channels into groups which can be addressed by a single group_id.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_get:

HTTPAPIWrapper.checked_get
---------------------------------------------------------------------------------------------------------------------



Calls self._checked_get_or_post with is_post=False..

.. raw:: html

  <embed>
  <head>
    <style>
        .style662 {
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
    <p class="style662">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.checked_get**(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)

.. raw:: html

  <embed>
  <head>
    <style>
        .style663 {
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
    <p class="style663">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **url:** Url.

* **the_request:** The request itself.

* **requests_kwargs=None:** The kwargs for the request.

* **good_message=None:** The message to print on a happy 200.

* **bad_message='This HTTPs GET request failed':** The message to print on a sad non-200.

* **raise_errors=True:** Whether to raise errors if sad.

.. raw:: html

  <embed>
  <head>
    <style>
        .style664 {
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
    <p class="style664">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The response. Raises a BadResponseException if it fails and raise_errors is set.

.. raw:: html

  <embed>
  <head>
    <style>
        .style665 {
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
    <p class="style665">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_post:

HTTPAPIWrapper.checked_post
---------------------------------------------------------------------------------------------------------------------



Calls self._checked_get_or_post with is_post=True..

.. raw:: html

  <embed>
  <head>
    <style>
        .style666 {
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
    <p class="style666">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.checked_post**(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)

.. raw:: html

  <embed>
  <head>
    <style>
        .style667 {
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
    <p class="style667">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **url:** Url.

* **the_request:** The request itself.

* **requests_kwargs=None:** The kwargs for the request.

* **good_message=None:** The message to print on a happy 200.

* **bad_message='This HTTPs POST request failed':** The message to print on a sad non-200.

* **raise_errors=True:** Whether to raise errors if sad.

.. raw:: html

  <embed>
  <head>
    <style>
        .style668 {
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
    <p class="style668">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The response. Raises a BadResponseException if it fails and raise_errors is set.

.. raw:: html

  <embed>
  <head>
    <style>
        .style669 {
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
    <p class="style669">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.headers:

HTTPAPIWrapper.headers
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style670 {
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
    <p class="style670">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.headers**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style671 {
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
    <p class="style671">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style672 {
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
    <p class="style672">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The authentication headers. Used for all API calls except for authenticate() and refresh().
headers["Auth-Origin"] is the authentication service, such as "cognito".
headers["Authorization"] is the access token, etc that proves authentication.

.. raw:: html

  <embed>
  <head>
    <style>
        .style673 {
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
    <p class="style673">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.authenticate:

HTTPAPIWrapper.authenticate
---------------------------------------------------------------------------------------------------------------------



Authenticates using self.username andself.password. Needs to be called before any other API calls.

.. raw:: html

  <embed>
  <head>
    <style>
        .style674 {
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
    <p class="style674">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.authenticate**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style675 {
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
    <p class="style675">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style676 {
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
    <p class="style676">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (the access token, the refresh token).
Raises an Exception if doesn't receive a valid response.
Like most GET and POST functions it will raise any errors thrown by the http API.

.. raw:: html

  <embed>
  <head>
    <style>
        .style677 {
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
    <p class="style677">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_up:

HTTPAPIWrapper.sign_up
---------------------------------------------------------------------------------------------------------------------



Signs up.

.. raw:: html

  <embed>
  <head>
    <style>
        .style678 {
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
    <p class="style678">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.sign_up**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style679 {
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
    <p class="style679">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style680 {
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
    <p class="style680">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (the access token, the refresh token).

.. raw:: html

  <embed>
  <head>
    <style>
        .style681 {
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
    <p class="style681">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.delete_account:

HTTPAPIWrapper.delete_account
---------------------------------------------------------------------------------------------------------------------



Deletes an account. Mainly used for testing.

.. raw:: html

  <embed>
  <head>
    <style>
        .style682 {
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
    <p class="style682">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.delete_account**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style683 {
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
    <p class="style683">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style684 {
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
    <p class="style684">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style685 {
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
    <p class="style685">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_out:

HTTPAPIWrapper.sign_out
---------------------------------------------------------------------------------------------------------------------



Signs out using the access token obtained from signing in.

.. raw:: html

  <embed>
  <head>
    <style>
        .style686 {
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
    <p class="style686">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.sign_out**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style687 {
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
    <p class="style687">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style688 {
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
    <p class="style688">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style689 {
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
    <p class="style689">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.refresh:

HTTPAPIWrapper.refresh
---------------------------------------------------------------------------------------------------------------------



Refreshes the access token.

.. raw:: html

  <embed>
  <head>
    <style>
        .style690 {
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
    <p class="style690">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.refresh**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style691 {
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
    <p class="style691">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style692 {
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
    <p class="style692">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The new token.

.. raw:: html

  <embed>
  <head>
    <style>
        .style693 {
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
    <p class="style693">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_character_profile:

HTTPAPIWrapper.fetch_character_profile
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style694 {
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
    <p class="style694">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_character_profile**(self, character_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style695 {
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
    <p class="style695">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **character_id:** String-valued (or list-valued) character_id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style696 {
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
    <p class="style696">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  Character object (or list therof),
It works for both member_ids and agent_ids.

.. raw:: html

  <embed>
  <head>
    <style>
        .style697 {
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
    <p class="style697">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_member_ids:

HTTPAPIWrapper.fetch_member_ids
---------------------------------------------------------------------------------------------------------------------



Fetches the member ids of a channel which coorespond to real users.

.. raw:: html

  <embed>
  <head>
    <style>
        .style698 {
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
    <p class="style698">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_member_ids**(self, channel_id, service_id, raise_empty_list_err)

.. raw:: html

  <embed>
  <head>
    <style>
        .style699 {
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
    <p class="style699">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** The channel ID.

* **service_id:** The service/client/user ID.

* **raise_empty_list_err=False:** Raises an Exception if the list is empty.

.. raw:: html

  <embed>
  <head>
    <style>
        .style700 {
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
    <p class="style700">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of character_id strings.

.. raw:: html

  <embed>
  <head>
    <style>
        .style701 {
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
    <p class="style701">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception (empty list) if raise_empty_list_err is True and the list is empty.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_agents:

HTTPAPIWrapper.fetch_agents
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style702 {
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
    <p class="style702">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_agents**(self, service_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style703 {
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
    <p class="style703">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** Service ID.

.. raw:: html

  <embed>
  <head>
    <style>
        .style704 {
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
    <p class="style704">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of non-user Character objects bound to this service.

.. raw:: html

  <embed>
  <head>
    <style>
        .style705 {
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
    <p class="style705">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_info:

HTTPAPIWrapper.fetch_user_info
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style706 {
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
    <p class="style706">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_user_info**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style707 {
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
    <p class="style707">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style708 {
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
    <p class="style708">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The UserInfo of the user logged in as, containing thier name, avatar, etc. Used by user mode.

.. raw:: html

  <embed>
  <head>
    <style>
        .style709 {
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
    <p class="style709">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_current_user:

HTTPAPIWrapper.update_current_user
---------------------------------------------------------------------------------------------------------------------



Updates the user info. Used by user mode.

.. raw:: html

  <embed>
  <head>
    <style>
        .style710 {
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
    <p class="style710">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.update_current_user**(self, avatar, description, name)

.. raw:: html

  <embed>
  <head>
    <style>
        .style711 {
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
    <p class="style711">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **avatar:** Link to image or local file_path to upload.

* **description:** Of the user.

* **name:** The name that shows in chat.

.. raw:: html

  <embed>
  <head>
    <style>
        .style712 {
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
    <p class="style712">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style713 {
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
    <p class="style713">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service:

HTTPAPIWrapper.create_service
---------------------------------------------------------------------------------------------------------------------



Creates and.

.. raw:: html

  <embed>
  <head>
    <style>
        .style714 {
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
    <p class="style714">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.create_service**(self, description)

.. raw:: html

  <embed>
  <head>
    <style>
        .style715 {
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
    <p class="style715">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **description:** Description string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style716 {
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
    <p class="style716">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The string-valued service_id.
Called once by the Moobius class if there is no service specified.

.. raw:: html

  <embed>
  <head>
    <style>
        .style717 {
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
    <p class="style717">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_service_id_list:

HTTPAPIWrapper.fetch_service_id_list
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style718 {
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
    <p class="style718">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_service_id_list**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style719 {
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
    <p class="style719">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style720 {
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
    <p class="style720">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of service_id strings of the user.

.. raw:: html

  <embed>
  <head>
    <style>
        .style721 {
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
    <p class="style721">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_agent:

HTTPAPIWrapper.create_agent
---------------------------------------------------------------------------------------------------------------------



Creates a character with a given name, avatar, and description.
The created user will be bound to the given service.

.. raw:: html

  <embed>
  <head>
    <style>
        .style722 {
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
    <p class="style722">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.create_agent**(self, service_id, name, avatar, description)

.. raw:: html

  <embed>
  <head>
    <style>
        .style723 {
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
    <p class="style723">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** The service_id/client_id.

* **name:** The name of the user.

* **avatar:** The image URL of the user's picture OR a local file path.

* **description:** The description of the user.

.. raw:: html

  <embed>
  <head>
    <style>
        .style724 {
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
    <p class="style724">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  Character object representing the created user.

.. raw:: html

  <embed>
  <head>
    <style>
        .style725 {
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
    <p class="style725">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_agent:

HTTPAPIWrapper.update_agent
---------------------------------------------------------------------------------------------------------------------



Updates the characters name, avatar, etc for a FAKE user, for real users use update_current_user.

.. raw:: html

  <embed>
  <head>
    <style>
        .style726 {
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
    <p class="style726">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.update_agent**(self, service_id, agent_id, avatar, description, name)

.. raw:: html

  <embed>
  <head>
    <style>
        .style727 {
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
    <p class="style727">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** Which service holds the user.

* **agent_id:** Who to update. Can also be a Character object. Cannot be a list.

* **avatar:** A link to user's image or a local file_path to upload.

* **description:** The description of user.

* **name:** The name that will show in chat.

.. raw:: html

  <embed>
  <head>
    <style>
        .style728 {
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
    <p class="style728">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The Data about the user as a dict.

.. raw:: html

  <embed>
  <head>
    <style>
        .style729 {
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
    <p class="style729">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel:

HTTPAPIWrapper.create_channel
---------------------------------------------------------------------------------------------------------------------



Creates a channel.

.. raw:: html

  <embed>
  <head>
    <style>
        .style730 {
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
    <p class="style730">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.create_channel**(self, channel_name, channel_desc)

.. raw:: html

  <embed>
  <head>
    <style>
        .style731 {
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
    <p class="style731">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_name:** String-valued channel name.

* **channel_desc:** Description.

.. raw:: html

  <embed>
  <head>
    <style>
        .style732 {
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
    <p class="style732">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The channel_id.
Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed".

.. raw:: html

  <embed>
  <head>
    <style>
        .style733 {
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
    <p class="style733">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.bind_service_to_channel:

HTTPAPIWrapper.bind_service_to_channel
---------------------------------------------------------------------------------------------------------------------



Binds a service to a channel.
This function is unusual in that it.

.. raw:: html

  <embed>
  <head>
    <style>
        .style734 {
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
    <p class="style734">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.bind_service_to_channel**(self, service_id, channel_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style735 {
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
    <p class="style735">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** Service.

* **channel_id:** Channel IDs.

.. raw:: html

  <embed>
  <head>
    <style>
        .style736 {
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
    <p class="style736">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* Whether it was sucessful rather than raising errors if it fails.

.. raw:: html

  <embed>
  <head>
    <style>
        .style737 {
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
    <p class="style737">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.unbind_service_from_channel:

HTTPAPIWrapper.unbind_service_from_channel
---------------------------------------------------------------------------------------------------------------------



Unbinds a service to a channel.

.. raw:: html

  <embed>
  <head>
    <style>
        .style738 {
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
    <p class="style738">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.unbind_service_from_channel**(self, service_id, channel_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style739 {
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
    <p class="style739">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **service_id:** Service.

* **channel_id:** Channel IDs.

.. raw:: html

  <embed>
  <head>
    <style>
        .style740 {
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
    <p class="style740">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style741 {
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
    <p class="style741">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel:

HTTPAPIWrapper.update_channel
---------------------------------------------------------------------------------------------------------------------



Updates the name and desc of a channel.

.. raw:: html

  <embed>
  <head>
    <style>
        .style742 {
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
    <p class="style742">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.update_channel**(self, channel_id, channel_name, channel_desc)

.. raw:: html

  <embed>
  <head>
    <style>
        .style743 {
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
    <p class="style743">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** Which channel to update.

* **channel_name:** The new channel name.

* **channel_desc:** The new channel description.

.. raw:: html

  <embed>
  <head>
    <style>
        .style744 {
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
    <p class="style744">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style745 {
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
    <p class="style745">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_popular_channels:

HTTPAPIWrapper.fetch_popular_channels
---------------------------------------------------------------------------------------------------------------------



Fetches the popular channels,.

.. raw:: html

  <embed>
  <head>
    <style>
        .style746 {
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
    <p class="style746">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_popular_channels**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style747 {
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
    <p class="style747">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style748 {
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
    <p class="style748">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of channel_id strings.

.. raw:: html

  <embed>
  <head>
    <style>
        .style749 {
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
    <p class="style749">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_list:

HTTPAPIWrapper.fetch_channel_list
---------------------------------------------------------------------------------------------------------------------



Fetches all? channels,.

.. raw:: html

  <embed>
  <head>
    <style>
        .style750 {
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
    <p class="style750">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_channel_list**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style751 {
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
    <p class="style751">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style752 {
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
    <p class="style752">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of channel_id strings.

.. raw:: html

  <embed>
  <head>
    <style>
        .style753 {
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
    <p class="style753">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_message_history:

HTTPAPIWrapper.fetch_message_history
---------------------------------------------------------------------------------------------------------------------



Returns the message chat history.

.. raw:: html

  <embed>
  <head>
    <style>
        .style754 {
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
    <p class="style754">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_message_history**(self, channel_id, limit, before)

.. raw:: html

  <embed>
  <head>
    <style>
        .style755 {
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
    <p class="style755">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** Channel with the messages inside of it.

* **limit=64:** Max number of messages to return (messages further back in time, if any, will not be returned).

* **before='null':** Only return messages older than this.

.. raw:: html

  <embed>
  <head>
    <style>
        .style756 {
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
    <p class="style756">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of dicts.

.. raw:: html

  <embed>
  <head>
    <style>
        .style757 {
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
    <p class="style757">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.this_user_channels:

HTTPAPIWrapper.this_user_channels
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style758 {
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
    <p class="style758">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.this_user_channels**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style759 {
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
    <p class="style759">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style760 {
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
    <p class="style760">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The list of channel_ids this user is in.

.. raw:: html

  <embed>
  <head>
    <style>
        .style761 {
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
    <p class="style761">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.upload:

HTTPAPIWrapper.upload
---------------------------------------------------------------------------------------------------------------------



Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.

.. raw:: html

  <embed>
  <head>
    <style>
        .style762 {
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
    <p class="style762">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.upload**(self, file_path)

.. raw:: html

  <embed>
  <head>
    <style>
        .style763 {
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
    <p class="style763">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **file_path:** File_path.

.. raw:: html

  <embed>
  <head>
    <style>
        .style764 {
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
    <p class="style764">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The uploaded URL. Raises an Exception if the upload fails.

.. raw:: html

  <embed>
  <head>
    <style>
        .style765 {
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
    <p class="style765">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.convert_to_url:

HTTPAPIWrapper.convert_to_url
---------------------------------------------------------------------------------------------------------------------



Uploads and.

.. raw:: html

  <embed>
  <head>
    <style>
        .style766 {
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
    <p class="style766">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.convert_to_url**(self, file_path)

.. raw:: html

  <embed>
  <head>
    <style>
        .style767 {
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
    <p class="style767">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **file_path:** File_path.

.. raw:: html

  <embed>
  <head>
    <style>
        .style768 {
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
    <p class="style768">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The bucket's url. Idempotent: If given a URL will just return the URL.
Empty, False, or None strings are converted to a default URL.

.. raw:: html

  <embed>
  <head>
    <style>
        .style769 {
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
    <p class="style769">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.download_size:

HTTPAPIWrapper.download_size
---------------------------------------------------------------------------------------------------------------------



Gets the download size in bytes. Queries for the header and does not download the file.

.. raw:: html

  <embed>
  <head>
    <style>
        .style770 {
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
    <p class="style770">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.download_size**(self, url, headers)

.. raw:: html

  <embed>
  <head>
    <style>
        .style771 {
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
    <p class="style771">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **url:** Url.

* **headers=None:** Optional headers.

.. raw:: html

  <embed>
  <head>
    <style>
        .style772 {
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
    <p class="style772">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The number of bytes.

.. raw:: html

  <embed>
  <head>
    <style>
        .style773 {
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
    <p class="style773">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.download:

HTTPAPIWrapper.download
---------------------------------------------------------------------------------------------------------------------



Downloads a file from a url or other source to a local filename, automatically creating dirs if need be.

.. raw:: html

  <embed>
  <head>
    <style>
        .style774 {
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
    <p class="style774">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.download**(self, source, file_path, auto_dir, overwrite, bytes, headers)

.. raw:: html

  <embed>
  <head>
    <style>
        .style775 {
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
    <p class="style775">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **source:** The url to download the file from. OR a MessageBody which has a .content.path in it.

* **file_path=None:** The file_path to download to.
    None will create a file based on the timestamp + random numbers.
    If no extension is specified, will infer the extension from the url if one exists.

* **auto_dir=None:** If no file_path is specified, a folder must be choosen.
    Defaults to './downloads'.

* **overwrite=None:** Allow overwriting pre-existing files. If False, will raise an Exception on name collision.

* **bytes=None:** If True, will return bytes instead of saving a file.

* **headers=None:** Optional headers. Use these for downloads that require auth.
    Can set to "self" to use the same auth headers that this instance is using.

.. raw:: html

  <embed>
  <head>
    <style>
        .style776 {
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
    <p class="style776">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The full filepath if bytes if false, otherwise the file's content bytes if bytes=True.

.. raw:: html

  <embed>
  <head>
    <style>
        .style777 {
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
    <p class="style777">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_dict:

HTTPAPIWrapper.fetch_channel_group_dict
---------------------------------------------------------------------------------------------------------------------



Similar to fetch_member_ids..

.. raw:: html

  <embed>
  <head>
    <style>
        .style778 {
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
    <p class="style778">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_channel_group_dict**(self, channel_id, service_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style779 {
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
    <p class="style779">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** Channel_id.

* **service_id:** Service_id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style780 {
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
    <p class="style780">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  dict from each group_id to all characters.

.. raw:: html

  <embed>
  <head>
    <style>
        .style781 {
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
    <p class="style781">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_list:

HTTPAPIWrapper.fetch_channel_group_list
---------------------------------------------------------------------------------------------------------------------



Similar to fetch_channel_group_dict..

.. raw:: html

  <embed>
  <head>
    <style>
        .style782 {
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
    <p class="style782">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_channel_group_list**(self, channel_id, service_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style783 {
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
    <p class="style783">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** Channel_id.

* **service_id:** Service_id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style784 {
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
    <p class="style784">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The raw data.

.. raw:: html

  <embed>
  <head>
    <style>
        .style785 {
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
    <p class="style785">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel_group:

HTTPAPIWrapper.create_channel_group
---------------------------------------------------------------------------------------------------------------------



Creates a channel group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style786 {
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
    <p class="style786">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.create_channel_group**(self, channel_id, group_name, members)

.. raw:: html

  <embed>
  <head>
    <style>
        .style787 {
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
    <p class="style787">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** The id of the group leader?.

* **group_name:** What to call it.

* **members:** A list of character_id strings that will be inside the group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style788 {
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
    <p class="style788">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The group_id string.

.. raw:: html

  <embed>
  <head>
    <style>
        .style789 {
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
    <p class="style789">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_service_group:

HTTPAPIWrapper.character_ids_of_service_group
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style790 {
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
    <p class="style790">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.character_ids_of_service_group**(self, group_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style791 {
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
    <p class="style791">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **group_id:** Group_id.

.. raw:: html

  <embed>
  <head>
    <style>
        .style792 {
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
    <p class="style792">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  list of character ids belonging to a service group.
Note that the 'recipients' in 'on message up' might be None:
  To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.

.. raw:: html

  <embed>
  <head>
    <style>
        .style793 {
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
    <p class="style793">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_channel_group:

HTTPAPIWrapper.character_ids_of_channel_group
---------------------------------------------------------------------------------------------------------------------



Gets a list of character ids belonging to a channel group.
Websocket payloads contain these channel_groups which are shorthand for a list of characters.

.. raw:: html

  <embed>
  <head>
    <style>
        .style794 {
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
    <p class="style794">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.character_ids_of_channel_group**(self, sender_id, channel_id, group_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style795 {
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
    <p class="style795">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **sender_id:** The message's sender.

* **channel_id:** The message specified that it was sent in this channel.

* **group_id:** The messages recipients.

.. raw:: html

  <embed>
  <head>
    <style>
        .style796 {
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
    <p class="style796">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The character_id list.

.. raw:: html

  <embed>
  <head>
    <style>
        .style797 {
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
    <p class="style797">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service_group:

HTTPAPIWrapper.create_service_group
---------------------------------------------------------------------------------------------------------------------



Creates a group containing the list of characters_ids and returns this Group object.
This group can then be used in send_message_down payloads.

.. raw:: html

  <embed>
  <head>
    <style>
        .style798 {
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
    <p class="style798">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.create_service_group**(self, members)

.. raw:: html

  <embed>
  <head>
    <style>
        .style799 {
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
    <p class="style799">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **members:** A list of character_id strings or Characters that will be inside the group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style800 {
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
    <p class="style800">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  Group object.

.. raw:: html

  <embed>
  <head>
    <style>
        .style801 {
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
    <p class="style801">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel_group:

HTTPAPIWrapper.update_channel_group
---------------------------------------------------------------------------------------------------------------------



Updates a channel group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style802 {
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
    <p class="style802">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.update_channel_group**(self, channel_id, group_id, members)

.. raw:: html

  <embed>
  <head>
    <style>
        .style803 {
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
    <p class="style803">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** The id of the group leader?.

* **group_id:** What to call it.

* **members:** A list of character_id strings that will be inside the group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style804 {
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
    <p class="style804">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style805 {
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
    <p class="style805">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception because it is unused, unimplemented, and may be removed.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_temp_channel_group:

HTTPAPIWrapper.update_temp_channel_group
---------------------------------------------------------------------------------------------------------------------



Updates a channel TEMP group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style806 {
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
    <p class="style806">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.update_temp_channel_group**(self, channel_id, members)

.. raw:: html

  <embed>
  <head>
    <style>
        .style807 {
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
    <p class="style807">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** The id of the group leader?.

* **members:** A list of character_id strings that will be inside the group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style808 {
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
    <p class="style808">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style809 {
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
    <p class="style809">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception because it is unused, unimplemented, and may be removed.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_temp_group:

HTTPAPIWrapper.fetch_channel_temp_group
---------------------------------------------------------------------------------------------------------------------



Like fetch_channel_group_list but for TEMP groups..

.. raw:: html

  <embed>
  <head>
    <style>
        .style810 {
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
    <p class="style810">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_channel_temp_group**(self, channel_id, service_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style811 {
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
    <p class="style811">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **channel_id:** Channel_id.

* **service_id:** Service_id,.

.. raw:: html

  <embed>
  <head>
    <style>
        .style812 {
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
    <p class="style812">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The list of groups.

.. raw:: html

  <embed>
  <head>
    <style>
        .style813 {
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
    <p class="style813">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_from_group:

HTTPAPIWrapper.fetch_user_from_group
---------------------------------------------------------------------------------------------------------------------



Not yet implemented!
Fetches the user profile of a user from a group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style814 {
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
    <p class="style814">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_user_from_group**(self, user_id, channel_id, group_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style815 {
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
    <p class="style815">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** The user ID.

* **channel_id:** The channel ID. (TODO: of what?).

* **group_id:** The group ID.

.. raw:: html

  <embed>
  <head>
    <style>
        .style816 {
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
    <p class="style816">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The user profile Character object.

.. raw:: html

  <embed>
  <head>
    <style>
        .style817 {
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
    <p class="style817">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception because it is unused, unimplemented, and may be removed.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_target_group:

HTTPAPIWrapper.fetch_target_group
---------------------------------------------------------------------------------------------------------------------



Not yet implemented!
Fetches info about the group.

.. raw:: html

  <embed>
  <head>
    <style>
        .style818 {
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
    <p class="style818">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.fetch_target_group**(self, user_id, channel_id, group_id)

.. raw:: html

  <embed>
  <head>
    <style>
        .style819 {
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
    <p class="style819">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **user_id:** The user id of the user bieng fetched (is this needed?).

* **channel_id:** The channel_id of the channel bieng fetched.

* **group_id:** Which group to fetch.

.. raw:: html

  <embed>
  <head>
    <style>
        .style820 {
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
    <p class="style820">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The data-dict data.

.. raw:: html

  <embed>
  <head>
    <style>
        .style821 {
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
    <p class="style821">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* An Exception because it is unused, unimplemented, and may be removed.



Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.network.http_api_wrapper_internal_attrs <moobius.network.http_api_wrapper_internal_attrs>
