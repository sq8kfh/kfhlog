kfhlog
======

Demo (heroku branch)
--------------------

http://kfhlog.herokuapp.com (user/password: test/test)

Getting Started
---------------

- Change directory into your newly created project.

    cd kfhlog

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_kfhlog_db production.ini
    env/bin/load_country_files production.ini

- Run your project's tests.

    env/bin/pytest

- Change auth.secret, dbsetting.secret and redis.sessions.secret in production.ini

- Run your project.

    env/bin/pserve production.ini
