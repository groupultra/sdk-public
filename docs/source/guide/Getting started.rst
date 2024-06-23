.. _getting-started-tut:

**Super fast** getting started
=================================
0. Get an account and create a channel.
1. Type these three lines into your shell: pip install moobius; python; from moobius import quickstart
2. Follow the instructions in the wizard.

**Fast** getting started
=================================

0. Get an account and create a channel.
1. pip install moobius
2. Copy the "template" example from "https://github.com/groupultra/sdk-public/tree/main/projects/template".
3. Rename the (example) service.py file to service.py
4. Fill in your credentials and the channel you created.

More details
=================================

There are several ingrediants:

* The moobius package installed with pip.
* A main.py that launches everything.
* A service.py that controls the behavior.
* Credentials for the service.py in a .gitignored place.
* A database.json file that controls the behavior of persistent database (optional, can set to the empty list []),
* For hybrid human/bot accounts, an agent.py, credentials, and it's own db.py file.

The main.py must call moobius.wand.run() to star the service, and it can start it either on the same or on a different process.

The service.py extends the class moobius.Moobius and overrides functions to implement it's own behavior.

The service.py also calls functions from this base class in order to tell the Platform to do stuff.
