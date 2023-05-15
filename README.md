Django Project Template
=======================

Features
--------
* Django 4
* Settings based on .env
* PostgreSQL DB settings
* Locales settings
* Static files in apps
* i18n settings
* Email settings for SendGrid
* File logging config (in logs/)
* Security options when not DEBUG
* Pre-commit hooks for 
  * Black
  * Ruff
* Basic configs for prospector, mypy, ruff

Usage
-----
1. Create DB (if you don't change name from .env then it's django_template)
2. Copy project/env/local.env to project/.env
3. Create venv by ./make-venv
4. Run migrations: ./venv/bin/python ./manage.py migrate
5. Start server: ./venv/bin/python ./manage.py runserver
6. Open in browser: http://127.0.0.1:8000/

Scripts
-------
* ./make-venv: Makes virtual environment (venv)
* ./msg: Combination of makemessages and compilemessages using locale/ directory
* ./test-coverage: Runs unit tests with test coverage report (using ``coverage`` tool)

