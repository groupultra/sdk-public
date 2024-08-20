
####################
Private functions
####################

.. _moobius.database.storage.get_engine._hit:

get_engine._hit
---------------------------------------------------------------------------------------------------------------------

* Signature

    * get_engine._hit(matches)

* Parameters

    * matches: List of matches.

* Returns

  * The if the engine is one of those matches.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__getitem__:

CachedDict.__getitem__
---------------------------------------------------------------------------------------------------------------------

Overrides dict-like usages of the form: "v = d['my_key']" to query from the database...

* Signature

    * CachedDict.__getitem__(self, key)

* Parameters

    * key: Key and.

* Returns

  * The value.

* Raises

  * A KeyError if strict_mode is True and the key is not found.

.. _moobius.database.storage.CachedDict.__setitem__:

CachedDict.__setitem__
---------------------------------------------------------------------------------------------------------------------

Overrides dict-like usages of the form: "d['my_key'] = v" to save to the database.
For a JSONDatabase, this will save the updated json to a file..

* Signature

    * CachedDict.__setitem__(self, key, value)

* Parameters

    * key: Key.
    
    * value: Value.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__delitem__:

CachedDict.__delitem__
---------------------------------------------------------------------------------------------------------------------

Overrides dict-like usages of the form: "del d['my_key']" to delete a key from the database.
For a JSONDatabase, this will save the updated json to a file..

* Signature

    * CachedDict.__delitem__(self, key)

* Parameters

    * key: Key.

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__str__:

CachedDict.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * CachedDict.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.CachedDict.__repr__:

CachedDict.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * CachedDict.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.MoobiusStorage.__str__:

MoobiusStorage.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * MoobiusStorage.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.database.storage.MoobiusStorage.__repr__:

MoobiusStorage.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * MoobiusStorage.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

####################
Private attributes
####################

get_engine._hit 

get_engine._hit 

get_engine._hit 
