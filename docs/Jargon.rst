.. _jargon-concepts-tut:

###################################################################################
Glossary of Jargon
###################################################################################

Here lies words specific (or nearly so) to Moobius and the concepts there in.

The service
==========================================

A **service** is an app that runs and controls all the behavior (except for agents).

The **dataclasses module** stores the types of all sorts of data that corresponds to users, UI, etc.

The **service_id** is created when a new service is created, which happens if the supplied service_id (in the JSON config) is an empty string.

Channels
==========================================
A **channel** is a chatroom threads. Channels are almost completly independant;
*every time* the service does anything, it must specify a channel it is performing it's action in.
A service can be bound to one or more channels.

A unique **channel_id** is auto-generated when a new channel is created.
Usually this is manually done, but it is possible to create a channel automatically.

Users
==========================================
Users can log into thier account and join a channel by entering it's secret ID. *Every time* the service does anything it also has to specify a list of of user-ids that see the change.

A **character** is a person/bot/puppet you see in the chat and can appear to send or recieve messages.
Each **Character** object cooresponds to the name, id, avatar, and description.

Each **member** is a character associated with a real account and channel; different channels have different *member_id* values even for the same user/bot.

Each **puppet** is a character puppeted by the service and is not associated with any channel.

An **Action** object is a generic "the user did something" for non-messages, etc.

An **avatar** is (a link to) an image that displays in the avatar.

A **user_id** is auto-generated on sign-up and stores the id of a user. There is only one per user regardless of which channels they join.

Buttons
==========================================
Buttons can be clicked on to do things.

A **Button** object is a representation of a button a user can click on.
*Simple buttons* just get clicked on but *complex buttons* open a pop-up menu.

A **ButtonClick** happens when the user clicks a button.

A **ButtonArgument** is used to describe a single element in the pop-up menu of a *complex-button*.

Messages
==========================================
These appear in the chat thread.

A **Message** object stores everything that is relevant to a message (who, when, and what).

A **MessageBody** object contains all the information.

The **message_type** of a message can be *text*, *image*, or *audio* for displayed content.
As well as a downloadable *file* or a *card* that links to a given url.

**message_up** messages are sent to the service by users and/or agents.

**message_down** messages are sent from the service to users and/or agents.

The Canvas
==========================================
This is the place to show text and/or images to the user without cluttering the chat.

The **Canvas** object contains a list of **CanvasElement** objects.

Each **CanvasElment** contains text and/or an image URLs to show on the page.

A list of **StyleElement** ojects is used to update the look-and feel.

The agent
==========================================

An **agent** is a bot that cooresponds to a user's account. Unlike a **puppet** it has autonomy.

Agents call **fetch** functions to query buttons, the canvas, and other information a user would see.

Agents send **message_up** messages back to the service.
