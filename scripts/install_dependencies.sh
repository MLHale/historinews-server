#!/bin/sh

export SCRIPTS_DIR=/opt/historinews-server/scripts

sudo apt-get update \
  && sudo apt-get -y install \
    apache2 \
    libapache2-mod-wsgi \
    libmagickwand-dev \
    python-pip \
    python-dev \
    git \
    postgresql \
    libpq-dev \
  && sudo pip install -r ${SCRIPTS_DIR}/requirements.txt
