
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
    <style>
        .style822 {
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
    <p class="style822">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper._checked_get_or_post**(self, url, the_request, is_post, requests_kwargs, good_message, bad_message, raise_errors)

.. raw:: html

  <embed>
  <head>
    <style>
        .style823 {
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
    <p class="style823">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **url:** The https://... url.

* **the_request:** The "json" kwarg is set to this. Can be None in which no "json" will be set.

* **is_post:** True for post, False for get.

* **requests_kwargs=None:** Dict of extra arguments to send to requests/aiohttp. None is equivalent to {}.

* **good_message=None:** The string-valued message to logger.debug. None means do not log.

* **bad_message='This HTTPs request failed':** The string-valued message to prepend to logger.error if the response isnt code 10000.

* **raise_errors=True:** Raise a BadResponseException if the request returns an error.

.. raw:: html

  <embed>
  <head>
    <style>
        .style824 {
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
    <p class="style824">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The https response as a dict, using requests/aiohttp.post(...).json() to parse it.

.. raw:: html

  <embed>
  <head>
    <style>
        .style825 {
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
    <p class="style825">
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
    <style>
        .style826 {
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
    <p class="style826">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper._xtract_character**(self, resp_data)

.. raw:: html

  <embed>
  <head>
    <style>
        .style827 {
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
    <p class="style827">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **resp_data:** JSON response data.

.. raw:: html

  <embed>
  <head>
    <style>
        .style828 {
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
    <p class="style828">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  Character object.

.. raw:: html

  <embed>
  <head>
    <style>
        .style829 {
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
    <p class="style829">
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
    <style>
        .style830 {
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
    <p class="style830">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper._upload_extension**(self, extension)

.. raw:: html

  <embed>
  <head>
    <style>
        .style831 {
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
    <p class="style831">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **extension:** String-valued extension.

.. raw:: html

  <embed>
  <head>
    <style>
        .style832 {
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
    <p class="style832">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* (upload_url or None, upload_fields).

.. raw:: html

  <embed>
  <head>
    <style>
        .style833 {
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
    <p class="style833">
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
    <style>
        .style834 {
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
    <p class="style834">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper._do_upload**(self, upload_url, upload_fields, file_path)

.. raw:: html

  <embed>
  <head>
    <style>
        .style835 {
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
    <p class="style835">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **upload_url:** Obtained with _upload_extension.

* **upload_fields:** Obtained with _upload_extension.

* **file_path:** The path of the file.

.. raw:: html

  <embed>
  <head>
    <style>
        .style836 {
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
    <p class="style836">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The full URL string of the uploaded file. None if doesn't receive a valid response (error condition).

.. raw:: html

  <embed>
  <head>
    <style>
        .style837 {
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
    <p class="style837">
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
    <style>
        .style838 {
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
    <p class="style838">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.__str__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style839 {
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
    <p class="style839">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style840 {
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
    <p class="style840">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style841 {
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
    <p class="style841">
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
    <style>
        .style842 {
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
    <p class="style842">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **HTTPAPIWrapper.__repr__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style843 {
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
    <p class="style843">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style844 {
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
    <p class="style844">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style845 {
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
    <p class="style845">
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
