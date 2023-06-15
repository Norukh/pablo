#! /bin/bash
sudo cp -r /images pablo_app/static/
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8080