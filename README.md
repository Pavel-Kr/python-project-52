### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pavel-Kr/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pavel-Kr/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/549890e87e6337b69c25/maintainability)](https://codeclimate.com/github/Pavel-Kr/python-project-52/maintainability)

# Task Manager

This is a simple task manager website, similar to [Redmine](https://www.redmine.org/).

This project is hosted on [Render](https://render.com/).

Link to the website: https://python-project-52-tyby.onrender.com/.

### How to run locally

Firstly, you need to install Poetry. Official installation guide can be found [here](https://python-poetry.org/docs/#installation).

Then you need to create a development version of the database. This project uses PostgreSQL. If you haven't install Postgres yet, follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04). To create development databse, run `make create-dev-db`. This will create a database, called `task_manager_db`. 

Then you need to set a password for this database and get connection info. For this, connect to newly created database, using `psql task_manager_db` command. This command will open a PostgreSQL shell, where you can configure your database. For now you will need only 2 commands: `\password` to set a password to your database and `\conninfo` to receive connection parameters.

Now, when you have all necessary information, open file `settings.py` in the `task_manager` folder, find `DATABASES` collection and replace link in the `default` parameter with your own link. Link should be constructed as `postgresql://<username>:<password>@<address>:<port>/<db_name>`. Usually, you would only need to replace username and password.

Now, when the development database is ready, run `make dev` to run a development web server.