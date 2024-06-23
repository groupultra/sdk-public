.. _jargon-concepts-tut:

Glossary of Jargon
===================================

Here lies words specific (or nearly so) to Moobius and the concepts there in.

The service
==========================================

A service is an app that runs and controls all the behavior (except for agents).

The **dataclasses module** stores the types of all sorts of data that corresponds to users, UI, etc.

The **service_id** is created when a new service is created, which happens if the supplied service_id (in the JSON config) is an empty string.

Channels
==========================================
Channels are independent chatroom threads. *Every time* the service does anything, it must specify a channel it is performing it's action in. A service can have one or more channels.

The **channel_id** is auto-generated when a new channel is created. Usually this is manually done, but it is possible to create a channel automatically.

Users
==========================================
Users can log into thier account and join a channel by entering it's secret ID. *Every time* the service does anything it also has to specify a list of of user-ids that see the change.

The **real characters** are ids associated with a real account.

The **virtual characters** are fake characters puppeted by the service.

A **Character** object is a representation of a character's name, id, avatar, and description.

An **Action** object is a generic "the user did something" for non-messags, etc.

An **Avatar** is (a link to) an image that displays in the avatar.

The **user_id** is auto-generated and stores the ID.

Buttons
==========================================
Buttons can be clicked on to do things.

A **Button** object is a. **Simple buttons** just get clicked on. **Complex buttons** open a pop-up menu.

A **ButtonClick** happens when the user clicks a button.

Messages
==========================================
These appear in the chat thread.

**message_up** messages are sent to the service.
**message_down** messages are sent from the service.

The Canvas
==========================================
This is the place to show text and/or images to the user without cluttering the chat.

The **Canvas** is a list of **CanvasElements** which are and/or image URLs to show on the page.

Updating the style with a **StyleElement** can specify whether the canvas is open or not. Note: This will be a fairly complex API.

The agent
==========================================
The agent is a bot which responds to updates recieved from the service.

Note: Do not use agents if you want virtual characters. Only use agents when you need *both* manual and automatic control of a character's behavior.
