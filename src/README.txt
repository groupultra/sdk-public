Moobius Python SDK version 0.0.1

Usage: 
1. Change current directory to `src`
2. Run `pip install . -e`. This command will install the package to your PYTHONPATH.
- Note: `-e` means editable mode. With this option your changes to the source code will be applied immediately.
3. Import the package in your code (Your code does not have to be in the same directory of `src/`): `import moobius`
4. Change current directory to `projects/test`
5. Edit `config.json`. Fill in your `email`, `password` and a list of `channels` you want to run on. If you have a `service_id`, just fill in the field, otherwise please use `"service_id": ""` and the SDK will create a new `service_id` for you. 
6. Run `python3 main.py`. The config file will automatically update so that you don't need to configure it the next time you start the program. You should expect a functional service in your band, that
- Has two Keys ("Meet Tubbs or Hermeowne" and "Meet Ms Fortune"). Both of them are functional.
- Will respond a "pong" to a "ping" message, and repeat other messages.
- Would Show "SYNC", "ASYNC", "BOMB" and "SURVIVE" messages automatically.