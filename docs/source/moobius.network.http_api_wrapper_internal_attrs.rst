
####################
Private functions
####################

.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._checked_get_or_post:

HTTPAPIWrapper._checked_get_or_post
---------------------------------------------------------------------------------------------------------------------



Runs a GET or POST request returning the result as a JSON with optional logging and error raising.

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

* **HTTPAPIWrapper._checked_get_or_post**(self, url, the_request, is_post, requests_kwargs, good_message, bad_message, raise_errors)

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

* __url:__ The https://... url.

* __the_request:__ The "json" kwarg is set to this. Can be None in which no "json" will be set.

* __is_post:__ True for post, False for get.

* __requests_kwargs=None:__ Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}.

* __good_message=None:__ The string-valued message to logger.debug. None means do not log.

* __bad_message='This HTTPs request failed':__ The string-valued message to prepend to logger.error if the response isnt code 10000.

* __raise_errors=True:__ Raise a BadResponseException if the request returns an error.

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

* The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

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

* BadResponseException if raise_errors=True and the response is an error response.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._xtract_character:

HTTPAPIWrapper._xtract_character
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

* **HTTPAPIWrapper._xtract_character**(self, resp_data)

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

* __resp_data:__ JSON response data.

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

* The  Character object.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._upload_extension:

HTTPAPIWrapper._upload_extension
---------------------------------------------------------------------------------------------------------------------



Gets the upload URL and needed fields for uploading a file.

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

* **HTTPAPIWrapper._upload_extension**(self, extension)

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

* __extension:__ String-valued extension.

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

* (upload_url or None, upload_fields).

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper._do_upload:

HTTPAPIWrapper._do_upload
---------------------------------------------------------------------------------------------------------------------



Uploads a file to the given upload URL with the given upload fields.

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

* **HTTPAPIWrapper._do_upload**(self, upload_url, upload_fields, file_path)

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

* __upload_url:__ Obtained with _upload_extension.

* __upload_fields:__ Obtained with _upload_extension.

* __file_path:__ The path of the file.

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

* The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

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

* Exception: If the file upload fails, this function will raise an exception detailing the error.



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__str__:

HTTPAPIWrapper.__str__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

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

* **HTTPAPIWrapper.__str__**(self)

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

* The  easy-to-read string summary.

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



.. _moobius.network.http_api_wrapper.HTTPAPIWrapper.__repr__:

HTTPAPIWrapper.__repr__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

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

* **HTTPAPIWrapper.__repr__**(self)

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

* The  easy-to-read string summary.

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



####################
Private attributes
####################

_URL2example_response

HTTPAPIWrapper._checked_get_or_post._URL2example_response 

HTTPAPIWrapper._do_upload._ 

HTTPAPIWrapper._checked_get_or_post._URL2example_response 
