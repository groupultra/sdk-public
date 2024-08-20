
####################
Private functions
####################

.. _moobius.core.sdk.Moobius._set_loguru:

Moobius._set_loguru
---------------------------------------------------------------------------------------------------------------------

Sets the log levels etc.  Set after setting self._config.

* Signature

    * Moobius._set_loguru(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius._convert_message_content:

Moobius._convert_message_content
---------------------------------------------------------------------------------------------------------------------

* Signature

    * Moobius._convert_message_content(self, subtype, content)

* Parameters

    * subtype: Subtype.
    
    * content: The string or dict-valued content,.

* Returns

  * The  MessageContent object.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius._update_rec:

Moobius._update_rec
---------------------------------------------------------------------------------------------------------------------

Use this function in the in the "recipients" fields of the websocket.
Converts lists into group_id strings, creating a group if need be, when.

* Signature

    * Moobius._update_rec(self, recipients, is_m_down, channel_id)

* Parameters

    * recipients: Recipients.
    
    * is_m_down: True if a message down.
    
    * channel_id=None: The channel_id.

* Returns

  * The converted list.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius._checkin:

Moobius._checkin
---------------------------------------------------------------------------------------------------------------------

Called as a rate task, used to resync users, etc. Only called after on_start().

* Signature

    * Moobius._checkin(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The None.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.__str__:

Moobius.__str__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * Moobius.__str__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.__repr__:

Moobius.__repr__
---------------------------------------------------------------------------------------------------------------------

The string output function for debugging.

* Signature

    * Moobius.__repr__(self)

* Parameters

    * (this class constructor accepts no arguments)

* Returns

  * The  easy-to-read string summary.

* Raises

  * (this function does not raise any notable errors)

.. _moobius.core.sdk.Moobius.handle_received_payload._group2ids:

Moobius.handle_received_payload._group2ids
---------------------------------------------------------------------------------------------------------------------

* Signature

    * Moobius.handle_received_payload._group2ids(g_id)

* Parameters

    * g_id: Gorup id.

* Returns

  * The  list of character id strings.

* Raises

  * (this function does not raise any notable errors)

####################
Private attributes
####################

Moobius.handle_received_payload._group2ids 

Moobius.handle_received_payload._group2ids 
