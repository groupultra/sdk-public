.. _getting-started-tut:

###################################################################################
Register, pip, run
###################################################################################


It is very easy to get Moobius started.
You can use your own computer as a server without any port-forwarding or other special network configurations.

If 24/7 reliability is important the service can be placed onto a cloud virtual machine instead.

**Super fast** getting started
=================================
0. Get an account.
1. Type this command using your credentials: `pip install moobius; python -m moobius my/folder -email email -password password`

**Very fast** getting started
=================================
0. Get an account and create a channel.
1. Type this command: `pip install moobius; python -m moobius -gui`
2. Follow the instructions in the wizard.

**Fast** getting started
=================================

0. Get an account and create a channel.
1. pip install moobius
2. Copy an example service such `as this template <https://github.com/groupultra/sdk-public/tree/main/projects/Template>`.
3. Fill in your credentials and the channel you created in the config/service.json file.

What is in a Moobus Service
=================================

There are several ingredents to make a service.

* The moobius package installed with pip.
* A main.py that launches everything.
The main.py calls `moobius.wand.run()`` to start the service, and it can start it either on the same process (blocking) or on a different process (non-blocking).

* A service.py that controls the behavior. **This is the main file you will be editing**.
The service.py extends the class moobius.Moobius and overrides functions to implement it's own behavior.
The service.py also calls functions from this base class in order to tell the Platform to do stuff.

* Credentials for your service; put these in a .gitignored place.
* An optiomal database.json file that controls the behavior of persistent database.
* For bot accounts, an agent.py with it's own credentials and it's own optional db.py file.

