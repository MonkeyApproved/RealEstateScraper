# RealEstateScraper

![Tests](https://github.com/MonkeyApproved/RealEstateScraper/actions/workflows/tests.yml/badge.svg)

To initialize the virtual environment with all dependencies simply run `source init.sh`.

## Django backend

The initial setup was done by adding *Django* to the requirements and installing it.
Afterwards run `django-admin startproject backend ./src` which created a new django project in our *src/* directory.
Now we can start the server by running `python src/manage.py runserver`.
