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
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **summarize_html**(html_str)

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

* __html_str:__ N html_string.

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

* The summary as a string.

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



.. _moobius.network.http_api_wrapper.get_or_post:

get_or_post
---------------------------------------------------------------------------------------------------------------------



Sends a GET or POST request and awaits for the response.

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

* **get_or_post**(url, is_post, requests_kwargs, raise_json_decode_errors)

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

* __url:__ Https://...

* __is_post:__ False for GET, True for POST.

* __requests_kwargs=None:__ These are fed into the requests/session get/post function.

* __raise_json_decode_errors=True:__ Raise errors parsing the JSON that the request sends back, otherwise return the error as a dict.

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
  </head>
  <body>
    <p class="fraises">
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
  </head>
  <body>
    <p class="fsig">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.checked_get**(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)

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

* __url:__ Url.

* __the_request:__ The request itself.

* __requests_kwargs=None:__ The kwargs for the request.

* __good_message=None:__ The message to print on a happy 200.

* __bad_message='This HTTPs GET request failed':__ The message to print on a sad non-200.

* __raise_errors=True:__ Whether to raise errors if sad.

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

* The response. Raises a BadResponseException if it fails and raise_errors is set.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.checked_post:

HTTPAPIWrapper.checked_post
---------------------------------------------------------------------------------------------------------------------



Calls self._checked_get_or_post with is_post=True..

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

* **HTTPAPIWrapper.checked_post**(self, url, the_request, requests_kwargs, good_message, bad_message, raise_errors)

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

* __url:__ Url.

* __the_request:__ The request itself.

* __requests_kwargs=None:__ The kwargs for the request.

* __good_message=None:__ The message to print on a happy 200.

* __bad_message='This HTTPs POST request failed':__ The message to print on a sad non-200.

* __raise_errors=True:__ Whether to raise errors if sad.

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

* The response. Raises a BadResponseException if it fails and raise_errors is set.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.headers:

HTTPAPIWrapper.headers
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.headers**(self)

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

* __(this class constructor accepts no arguments):__

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

* The authentication headers. Used for all API calls except for authenticate() and refresh().
headers["Auth-Origin"] is the authentication service, such as "cognito".
headers["Authorization"] is the access token, etc that proves authentication.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.authenticate:

HTTPAPIWrapper.authenticate
---------------------------------------------------------------------------------------------------------------------



Authenticates using self.username andself.password. Needs to be called before any other API calls.

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

* **HTTPAPIWrapper.authenticate**(self)

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

* __(this class constructor accepts no arguments):__

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

* (the access token, the refresh token).
Raises an Exception if doesn't receive a valid response.
Like most GET and POST functions it will raise any errors thrown by the http API.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.request_sign_up_code:

HTTPAPIWrapper.request_sign_up_code
---------------------------------------------------------------------------------------------------------------------



Signs up and sends the confirmation code to the email.  After confirming the account, self.authenticate() can be used to retrieve access and refresh tokens.

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

* **HTTPAPIWrapper.request_sign_up_code**(self)

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

* __(this class constructor accepts no arguments):__

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.request_sign_up_code_again:

HTTPAPIWrapper.request_sign_up_code_again
---------------------------------------------------------------------------------------------------------------------



Resends the confimation code.  After confirming the account, self.authenticate() can be used to retrieve access and refresh tokens.

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

* **HTTPAPIWrapper.request_sign_up_code_again**(self)

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

* __(this class constructor accepts no arguments):__

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_up_with_code:

HTTPAPIWrapper.sign_up_with_code
---------------------------------------------------------------------------------------------------------------------



Sends the confirmation code confirming the signup itself..  After confirming the account, self.authenticate() can be used to retrieve access and refresh tokens.

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

* **HTTPAPIWrapper.sign_up_with_code**(self, the_code)

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

* __the_code:__ Sign up code that was emailed.

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.get_password_reset_code:

HTTPAPIWrapper.get_password_reset_code
---------------------------------------------------------------------------------------------------------------------



Sends a reset-password request to the platform. After such a request is sent it will be necessary to check the email.

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

* **HTTPAPIWrapper.get_password_reset_code**(self)

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

* __(this class constructor accepts no arguments):__

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.reset_password:

HTTPAPIWrapper.reset_password
---------------------------------------------------------------------------------------------------------------------



Updates the password with a new one..

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

* **HTTPAPIWrapper.reset_password**(self, the_code)

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

* __the_code:__ Code that was emailed to the user (use get_password_reset_code).

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.delete_account:

HTTPAPIWrapper.delete_account
---------------------------------------------------------------------------------------------------------------------



Deletes the currently signed in account. Mainly used for testing.

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

* **HTTPAPIWrapper.delete_account**(self)

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

* __(this class constructor accepts no arguments):__

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.sign_out:

HTTPAPIWrapper.sign_out
---------------------------------------------------------------------------------------------------------------------



Signs out using the access token obtained from signing in.

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

* **HTTPAPIWrapper.sign_out**(self)

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

* __(this class constructor accepts no arguments):__

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.refresh:

HTTPAPIWrapper.refresh
---------------------------------------------------------------------------------------------------------------------



Refreshes the access token.

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

* **HTTPAPIWrapper.refresh**(self)

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

* __(this class constructor accepts no arguments):__

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

* The new token.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_character_profile:

HTTPAPIWrapper.fetch_character_profile
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.fetch_character_profile**(self, character)

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

* __character:__ String-valued (or list-valued) character_id/character.

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

* The  Character object (or list therof).
It works for both member_ids and agent_ids.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_member_ids:

HTTPAPIWrapper.fetch_member_ids
---------------------------------------------------------------------------------------------------------------------



Fetches the member ids of a channel which coorespond to real users.

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

* **HTTPAPIWrapper.fetch_member_ids**(self, channel_id, service_id, raise_empty_list_err)

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

* __channel_id:__ The channel ID.

* __service_id:__ The service/client/user ID.

* __raise_empty_list_err=False:__ Raises an Exception if the list is empty.

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

* The  list of character_id strings.

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

* An Exception (empty list) if raise_empty_list_err is True and the list is empty.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_agents:

HTTPAPIWrapper.fetch_agents
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.fetch_agents**(self, service_id)

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

* __service_id:__ Service ID.

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

* The  list of non-user Character objects bound to this service.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_info:

HTTPAPIWrapper.fetch_user_info
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.fetch_user_info**(self)

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

* __(this class constructor accepts no arguments):__

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

* The UserInfo of the user logged in as, containing thier name, avatar, etc. Used by user mode.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_current_user:

HTTPAPIWrapper.update_current_user
---------------------------------------------------------------------------------------------------------------------



Updates the user info. Used by user mode.

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

* **HTTPAPIWrapper.update_current_user**(self, avatar, description, name)

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

* __avatar:__ Link to image or local file_path to upload.

* __description:__ Of the user.

* __name:__ The name that shows in chat.

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service:

HTTPAPIWrapper.create_service
---------------------------------------------------------------------------------------------------------------------



Creates and.

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

* **HTTPAPIWrapper.create_service**(self, description)

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

* __description:__ Description string.

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

* The string-valued service_id.
Called once by the Moobius class if there is no service specified.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_service_id_list:

HTTPAPIWrapper.fetch_service_id_list
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.fetch_service_id_list**(self)

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

* __(this class constructor accepts no arguments):__

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

* The  list of service_id strings of the user.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_agent:

HTTPAPIWrapper.create_agent
---------------------------------------------------------------------------------------------------------------------



Creates a character with a given name, avatar, and description.
The created user will be bound to the given service.

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

* **HTTPAPIWrapper.create_agent**(self, service_id, name, avatar, description)

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

* __service_id:__ The service_id/client_id.

* __name:__ The name of the user.

* __avatar:__ The image URL of the user's picture OR a local file path.

* __description:__ The description of the user.

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

* The  Character object representing the created user.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_agent:

HTTPAPIWrapper.update_agent
---------------------------------------------------------------------------------------------------------------------



Updates the characters name, avatar, etc for a FAKE user, for real users use update_current_user.

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

* **HTTPAPIWrapper.update_agent**(self, service_id, character, avatar, description, name)

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

* __service_id:__ The service_id/client_id.

* __character:__ Who to update. Can also be a Character object or character_id. Cannot be a list.

* __avatar:__ A link to user's image or a local file_path to upload.

* __description:__ The description of user.

* __name:__ The name that will show in chat.

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

* The Data about the user as a dict.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel:

HTTPAPIWrapper.create_channel
---------------------------------------------------------------------------------------------------------------------



Creates a channel.

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

* **HTTPAPIWrapper.create_channel**(self, channel_name, channel_desc)

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

* __channel_name:__ String-valued channel name.

* __channel_desc:__ Description.

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

* The channel_id.
Example ID: "13e44ea3-b559-45af-9106-6aa92501d4ed".

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.bind_service_to_channel:

HTTPAPIWrapper.bind_service_to_channel
---------------------------------------------------------------------------------------------------------------------



Binds a service to a channel.
This function is unusual in that it.

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

* **HTTPAPIWrapper.bind_service_to_channel**(self, service_id, channel_id)

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

* __service_id:__ Service.

* __channel_id:__ Channel IDs.

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

* Whether it was sucessful rather than raising errors if it fails.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.unbind_service_from_channel:

HTTPAPIWrapper.unbind_service_from_channel
---------------------------------------------------------------------------------------------------------------------



Unbinds a service to a channel.

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

* **HTTPAPIWrapper.unbind_service_from_channel**(self, service_id, channel_id)

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

* __service_id:__ Service.

* __channel_id:__ Channel IDs.

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel:

HTTPAPIWrapper.update_channel
---------------------------------------------------------------------------------------------------------------------



Updates the name and desc of a channel.

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

* **HTTPAPIWrapper.update_channel**(self, channel_id, channel_name, channel_desc)

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

* __channel_id:__ Which channel to update.

* __channel_name:__ The new channel name.

* __channel_desc:__ The new channel description.

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

* None.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_popular_channels:

HTTPAPIWrapper.fetch_popular_channels
---------------------------------------------------------------------------------------------------------------------



Fetches the popular channels,.

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

* **HTTPAPIWrapper.fetch_popular_channels**(self)

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

* __(this class constructor accepts no arguments):__

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

* The  list of channel_id strings.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_list:

HTTPAPIWrapper.fetch_channel_list
---------------------------------------------------------------------------------------------------------------------



Fetches all? channels,.

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

* **HTTPAPIWrapper.fetch_channel_list**(self)

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

* __(this class constructor accepts no arguments):__

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

* The  list of channel_id strings.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_message_history:

HTTPAPIWrapper.fetch_message_history
---------------------------------------------------------------------------------------------------------------------



Returns the message chat history.

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

* **HTTPAPIWrapper.fetch_message_history**(self, channel_id, limit, before)

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

* __channel_id:__ Channel with the messages inside of it.

* __limit=64:__ Max number of messages to return (messages further back in time, if any, will not be returned).

* __before='null':__ Only return messages older than this.

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

* The  list of dicts.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.this_user_channels:

HTTPAPIWrapper.this_user_channels
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.this_user_channels**(self)

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

* __(this class constructor accepts no arguments):__

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

* The list of channel_ids this user is in.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.upload:

HTTPAPIWrapper.upload
---------------------------------------------------------------------------------------------------------------------



Uploads the file at local path file_path to the Moobius server. Automatically calculates the upload URL and upload fields.

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

* **HTTPAPIWrapper.upload**(self, file_path)

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

* __file_path:__ File_path.

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

* The uploaded URL. Raises an Exception if the upload fails.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.convert_to_url:

HTTPAPIWrapper.convert_to_url
---------------------------------------------------------------------------------------------------------------------



Uploads and.

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

* **HTTPAPIWrapper.convert_to_url**(self, file_path)

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

* __file_path:__ File_path.

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

* The bucket's url. Idempotent: If given a URL will just return the URL.
Empty, False, or None strings are converted to a default URL.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.download_size:

HTTPAPIWrapper.download_size
---------------------------------------------------------------------------------------------------------------------



Gets the download size in bytes. Queries for the header and does not download the file.

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

* **HTTPAPIWrapper.download_size**(self, url, headers)

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

* __url:__ Url.

* __headers=None:__ Optional headers.

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

* The number of bytes.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.download:

HTTPAPIWrapper.download
---------------------------------------------------------------------------------------------------------------------



Downloads a file from a url or other source to a local filename, automatically creating dirs if need be.

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

* **HTTPAPIWrapper.download**(self, source, file_path, auto_dir, overwrite, bytes, headers)

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

* __source:__ The url to download the file from. OR a MessageBody which has a .content.path in it.

* __file_path=None:__ The file_path to download to.
    None will create a file based on the timestamp + random numbers.
    If no extension is specified, will infer the extension from the url if one exists.

* __auto_dir=None:__ If no file_path is specified, a folder must be choosen.
    Defaults to './downloads'.

* __overwrite=None:__ Allow overwriting pre-existing files. If False, will raise an Exception on name collision.

* __bytes=None:__ If True, will return bytes instead of saving a file.

* __headers=None:__ Optional headers. Use these for downloads that require auth.
    Can set to "self" to use the same auth headers that this instance is using.

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

* The full filepath if bytes if false, otherwise the file's content bytes if bytes=True.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_dict:

HTTPAPIWrapper.fetch_channel_group_dict
---------------------------------------------------------------------------------------------------------------------



Similar to fetch_member_ids..

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

* **HTTPAPIWrapper.fetch_channel_group_dict**(self, channel_id, service_id)

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

* __channel_id:__ Channel_id.

* __service_id:__ Service_id.

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

* The  dict from each group_id to all characters.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_group_list:

HTTPAPIWrapper.fetch_channel_group_list
---------------------------------------------------------------------------------------------------------------------



Similar to fetch_channel_group_dict..

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

* **HTTPAPIWrapper.fetch_channel_group_list**(self, channel_id, service_id)

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

* __channel_id:__ Channel_id.

* __service_id:__ Service_id.

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

* The raw data.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_channel_group:

HTTPAPIWrapper.create_channel_group
---------------------------------------------------------------------------------------------------------------------



Creates a channel group.

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

* **HTTPAPIWrapper.create_channel_group**(self, channel_id, group_name, characters)

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

* __channel_id:__ The id of the group leader?.

* __group_name:__ What to call it.

* __characters:__ A list of characters or character_id strings that will be inside the group.

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

* The group_id string.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_service_group:

HTTPAPIWrapper.character_ids_of_service_group
---------------------------------------------------------------------------------------------------------------------



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

* **HTTPAPIWrapper.character_ids_of_service_group**(self, group_id)

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

* The  list of character ids belonging to a service group.
Note that the 'recipients' in 'on message up' might be None:
  To avoid requiring checks for None this function will return an empty list given Falsey inputs or Falsey string literals.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.character_ids_of_channel_group:

HTTPAPIWrapper.character_ids_of_channel_group
---------------------------------------------------------------------------------------------------------------------



Gets a list of character ids belonging to a channel group.
Websocket payloads contain these channel_groups which are shorthand for a list of characters.

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

* **HTTPAPIWrapper.character_ids_of_channel_group**(self, sender_id, channel_id, group_id)

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

* __sender_id:__ The message's sender.

* __channel_id:__ The message specified that it was sent in this channel.

* __group_id:__ The messages recipients.

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

* The character_id list.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.create_service_group:

HTTPAPIWrapper.create_service_group
---------------------------------------------------------------------------------------------------------------------



Creates a group containing the list of characters_ids and returns this Group object.
This group can then be used in send_message_down payloads.

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

* **HTTPAPIWrapper.create_service_group**(self, characters)

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

* __characters:__ A list of character_id strings or Characters that will be inside the group.

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

* The  Group object.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_channel_group:

HTTPAPIWrapper.update_channel_group
---------------------------------------------------------------------------------------------------------------------



Updates a channel group.

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

* **HTTPAPIWrapper.update_channel_group**(self, channel_id, group_id, characters)

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

* __channel_id:__ The id of the group leader?.

* __group_id:__ What to call it.

* __characters:__ A list of character_id strings that will be inside the group.

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

* None.

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

* An Exception because it is unused, unimplemented, and may be removed.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.update_temp_channel_group:

HTTPAPIWrapper.update_temp_channel_group
---------------------------------------------------------------------------------------------------------------------



Updates a channel TEMP group.

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

* **HTTPAPIWrapper.update_temp_channel_group**(self, channel_id, characters)

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

* __channel_id:__ The id of the group leader?.

* __characters:__ A list of character_id strings that will be inside the group.

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

* None.

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

* An Exception because it is unused, unimplemented, and may be removed.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_channel_temp_group:

HTTPAPIWrapper.fetch_channel_temp_group
---------------------------------------------------------------------------------------------------------------------



Like fetch_channel_group_list but for TEMP groups..

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

* **HTTPAPIWrapper.fetch_channel_temp_group**(self, channel_id, service_id)

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

* __channel_id:__ Channel_id.

* __service_id:__ Service_id,.

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

* The list of groups.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_user_from_group:

HTTPAPIWrapper.fetch_user_from_group
---------------------------------------------------------------------------------------------------------------------



Not yet implemented!
Fetches the user profile of a user from a group.

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

* **HTTPAPIWrapper.fetch_user_from_group**(self, user_id, channel_id, group_id)

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

* __user_id:__ The user ID.

* __channel_id:__ The channel ID. (TODO: of what?).

* __group_id:__ The group ID.

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

* The user profile Character object.

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

* An Exception because it is unused, unimplemented, and may be removed.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.fetch_target_group:

HTTPAPIWrapper.fetch_target_group
---------------------------------------------------------------------------------------------------------------------



Not yet implemented!
Fetches info about the group.

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

* **HTTPAPIWrapper.fetch_target_group**(self, user_id, channel_id, group_id)

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

* __user_id:__ The user id of the user bieng fetched (is this needed?).

* __channel_id:__ The channel_id of the channel bieng fetched.

* __group_id:__ Which group to fetch.

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

* The data-dict data.

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

* An Exception because it is unused, unimplemented, and may be removed.



Class attributes
--------------------



**********************
Internals
**********************
.. toctree::
   :maxdepth: 2

   moobius.network.http_api_wrapper_internal_attrs <moobius.network.http_api_wrapper_internal_attrs>
