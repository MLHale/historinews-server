#!/bin/sh

export ROOT_DIR=/opt/historinews-server

sudo -u postgres psql -c "DROP DATABASE historinews;"
rm ${ROOT_DIR}/historinews/api/migrations/0*
sudo rm ${ROOT_DIR}/historinews/pdfs/*
cd ${ROOT_DIR} \
  && python generate_secrets.py \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py createsuperuser
