rm -rf weighttrackingapi/migrations
rm db.sqlite3
python manage.py makemigrations weighttrackingapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata employees
python manage.py loaddata residents
python manage.py loaddata weight_sheets
python manage.py loaddata weights
python manage.py loaddata messages
python manage.py loaddata employee_messages

