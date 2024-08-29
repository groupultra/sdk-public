
####################
Private functions
####################

.. _moobius.database.storage.get_engine._hit:

get_engine._hit
---------------------------------------------------------------------------------------------------------------------



.. raw:: html

  <embed>
  <head>
    <style>
        .style622 {
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
    <p class="style622">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **get_engine._hit**(matches)

.. raw:: html

  <embed>
  <head>
    <style>
        .style623 {
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
    <p class="style623">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **matches:** List of matches.

.. raw:: html

  <embed>
  <head>
    <style>
        .style624 {
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
    <p class="style624">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The if the engine is one of those matches.

.. raw:: html

  <embed>
  <head>
    <style>
        .style625 {
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
    <p class="style625">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.__getitem__:

CachedDict.__getitem__
---------------------------------------------------------------------------------------------------------------------



Overrides dict-like usages of the form: "v = d['my_key']" to query from the database...

.. raw:: html

  <embed>
  <head>
    <style>
        .style626 {
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
    <p class="style626">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.__getitem__**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style627 {
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
    <p class="style627">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key and.

.. raw:: html

  <embed>
  <head>
    <style>
        .style628 {
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
    <p class="style628">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style629 {
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
    <p class="style629">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* A KeyError if strict_mode is True and the key is not found.



.. _moobius.database.storage.CachedDict.__setitem__:

CachedDict.__setitem__
---------------------------------------------------------------------------------------------------------------------



Overrides dict-like usages of the form: "d['my_key'] = v" to save to the database.
For a JSONDatabase, this will save the updated json to a file..

.. raw:: html

  <embed>
  <head>
    <style>
        .style630 {
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
    <p class="style630">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.__setitem__**(self, key, value)

.. raw:: html

  <embed>
  <head>
    <style>
        .style631 {
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
    <p class="style631">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

* **value:** Value.

.. raw:: html

  <embed>
  <head>
    <style>
        .style632 {
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
    <p class="style632">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style633 {
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
    <p class="style633">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.__delitem__:

CachedDict.__delitem__
---------------------------------------------------------------------------------------------------------------------



Overrides dict-like usages of the form: "del d['my_key']" to delete a key from the database.
For a JSONDatabase, this will save the updated json to a file..

.. raw:: html

  <embed>
  <head>
    <style>
        .style634 {
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
    <p class="style634">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.__delitem__**(self, key)

.. raw:: html

  <embed>
  <head>
    <style>
        .style635 {
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
    <p class="style635">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **key:** Key.

.. raw:: html

  <embed>
  <head>
    <style>
        .style636 {
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
    <p class="style636">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* None.

.. raw:: html

  <embed>
  <head>
    <style>
        .style637 {
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
    <p class="style637">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.__str__:

CachedDict.__str__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

.. raw:: html

  <embed>
  <head>
    <style>
        .style638 {
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
    <p class="style638">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.__str__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style639 {
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
    <p class="style639">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style640 {
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
    <p class="style640">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style641 {
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
    <p class="style641">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.CachedDict.__repr__:

CachedDict.__repr__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

.. raw:: html

  <embed>
  <head>
    <style>
        .style642 {
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
    <p class="style642">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **CachedDict.__repr__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style643 {
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
    <p class="style643">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style644 {
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
    <p class="style644">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style645 {
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
    <p class="style645">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.MoobiusStorage.__str__:

MoobiusStorage.__str__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

.. raw:: html

  <embed>
  <head>
    <style>
        .style646 {
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
    <p class="style646">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusStorage.__str__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style647 {
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
    <p class="style647">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style648 {
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
    <p class="style648">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style649 {
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
    <p class="style649">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



.. _moobius.database.storage.MoobiusStorage.__repr__:

MoobiusStorage.__repr__
---------------------------------------------------------------------------------------------------------------------



The string output function for debugging.

.. raw:: html

  <embed>
  <head>
    <style>
        .style650 {
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
    <p class="style650">
          <b>Signature:</b>
    </p>
  </body>
  </embed>

* **MoobiusStorage.__repr__**(self)

.. raw:: html

  <embed>
  <head>
    <style>
        .style651 {
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
    <p class="style651">
          <b>Parameters:</b>
    </p>
  </body>
  </embed>

* **(this class constructor accepts no arguments):**

.. raw:: html

  <embed>
  <head>
    <style>
        .style652 {
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
    <p class="style652">
          <b>Returns:</b>
    </p>
  </body>
  </embed>

* The  easy-to-read string summary.

.. raw:: html

  <embed>
  <head>
    <style>
        .style653 {
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
    <p class="style653">
          <b>Raises:</b>
    </p>
  </body>
  </embed>

* (this function does not raise any notable errors)



####################
Private attributes
####################

get_engine._hit 

get_engine._hit 

get_engine._hit 
