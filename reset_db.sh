# delete all migrations
echo ">>> removing all migration files from project"
find . -path "./src/*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "./src/*/migrations/*.pyc"  -delete

# delete database
echo ">>> removing sqlite database"
rm ./src/db.sqlite3

# create new database with updated model
echo ">>> migrate current models"
python src/manage.py makemigrations
python src/manage.py migrate

# add default super-user (user: admin, password: admin)
echo ">>> create new super user (user: admin, password: admin)"
echo ">>> THIS IS ONLY FOR LOCAL DEV! DO NOT USE FOR DEPLOYED VERSION!"
export DJANGO_SUPERUSER_PASSWORD="admin"
python src/manage.py createsuperuser --email "monkeyapprovedmonkey@gmail.com" --username "admin" --no-input
