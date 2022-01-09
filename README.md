# RealEstateScraper

![Tests](https://github.com/MonkeyApproved/RealEstateScraper/actions/workflows/tests.yml/badge.svg)

To initialize the virtual environment with all dependencies simply run `source init.sh`.

## Django backend

The initial setup was done by adding *Django* to the requirements and installing it.
Afterwards run `django-admin startproject <project name> ./src` which created a new django project in our *src/* directory.
Now we can start the server by running `python src/manage.py runserver`.

In order to add an App we use `python src/manage.py startapp <app name>` which initializes a new app.

### Routes

All routes are defined in the *urls.py* files in *backend/* and the app directories.
The main entry point is *backend/urls.py* from where calls can be directed to the *urls.py* files in the app directories.

### Database models

In order to apply a new model, we first run `python src/manage.py makemigrations`.
This will create a new migration file in the migrations folder of the App.
We can also check out the actual SQL command this will create, by running `python src/manage.py sqlmigrate <app-name> <migration id>` (replace `0001` with the id of the migration).
Afterwards in order to apply the migration to our database, we run `python src/manage.py migrate`.
