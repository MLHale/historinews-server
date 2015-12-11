#!/bin/sh

export ROOT_DIR=/opt/historinews-server
export STATIC_DIR=${ROOT_DIR}/historinews/static
export DJANGO_STATIC_DIR=/usr/local/lib/python2.7/dist-packages/django/contrib/admin/static
export REST_FRAMEWORK_CSS_DIR=/usr/local/lib/python2.7/dist-packages/rest_framework/static/rest_framework
export APACHE_CONFIG=/etc/apache2/sites-enabled/000-default.conf

sudo cp ${ROOT_DIR}/000-default.conf ${APACHE_CONFIG}

cp -R ${REST_FRAMEWORK_CSS_DIR} ${STATIC_DIR}/rest_framework
sudo chown -R ${USER}:www-data ${ROOT_DIR}/historinews/pdfs/

cd ${ROOT_DIR} \
  && python generate_secrets.py /opt/historinews-server/historinews/secret.py \
  && python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py createsuperuser
