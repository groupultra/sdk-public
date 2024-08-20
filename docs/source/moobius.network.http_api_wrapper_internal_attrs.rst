
####################
Private functions
####################

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._checked_get_or_post:

HTTPAPIWrapper._checked_get_or_post
---------------------------------------------------------------------------------------------------------------------

Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

* Signature

    * HTTPAPIWrapper._checked_get_or_post(self, url, the_request, is_post, requests_kwargs, good_message, bad_message, raise_errors)

* Parameters

    * url: The https://... url.
    
    * the_request: The "json" kwarg is set to this. Can be None in which no "json" will be set.
    
    * is_post: True for post, False for get.
    
    * requests_kwargs=None: Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}.
    
    * good_message=None: The string-valued message to logger.debug. None means do not log.
    
    * bad_message='This HTTPs request failed': The string-valued message to prepend to logger.error if the response isnt code 10000.
    
    * raise_errors=True: Raise a BadResponseException if the request returns an error.

* Returns

  * The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

* Raises

  * BadResponseException if raise_errors=True and the response is an error response.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._xtract_character:

HTTPAPIWrapper._xtract_character
---------------------------------------------------------------------------------------------------------------------

* Signature

    * HTTPAPIWrapper._xtract_character(self, resp_data)

* Parameters

    * resp_data: JSON response data.

* Returns

  * The  Character object.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._upload_extension:

HTTPAPIWrapper._upload_extension
---------------------------------------------------------------------------------------------------------------------

Gets the upload URL and needed fields for uploading a file.

* Signature

    * HTTPAPIWrapper._upload_extension(self, extension)

* Parameters

    * extension: String-valued extension.

* Returns

  * (upload_url or None, upload_fields).

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._do_upload:

HTTPAPIWrapper._do_upload
---------------------------------------------------------------------------------------------------------------------

Uploads a file to the given upload URL with the given upload fields.

* Signature

    * HTTPAPIWrapper._do_upload(self, upload_url, upload_fields, file_path)

* Parameters

    * upload_url: Obtained with _upload_extension.
    
    * upload_fields: Obtained with _upload_extension.
    
    * file_path: The path of the file.

* Returns

  * The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

* Raises

  * Exception: If the file upload fails, this function will raise an exception detailing the error.

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__str__:

HTTPAPIWrapper.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * HTTPAPIWrapper.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__repr__:

HTTPAPIWrapper.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * HTTPAPIWrapper.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

####################
Private attributes
####################

_URL2example_response

HTTPAPIWrapper._checked_get_or_post._URL2example_response 

HTTPAPIWrapper._do_upload._ 

HTTPAPIWrapper._checked_get_or_post._URL2example_response 
