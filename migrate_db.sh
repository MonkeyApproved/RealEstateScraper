# update database models
echo ">>> migrate current models"
python src/manage.py makemigrations
python src/manage.py migrate
