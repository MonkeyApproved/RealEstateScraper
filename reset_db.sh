# delete all migrations
find . -path "./src/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# delete database
rm ./src/db.sqlite3

# create new database with updated model
python src/manage.py makemigrations
python src/manage.py migrate
