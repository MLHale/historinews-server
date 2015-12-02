#!/bin/sh

export SCRIPTS_DIR=/opt/historinews-server/scripts

${SCRIPTS_DIR}/install_dependencies.sh \
  && ${SCRIPTS_DIR}/build.sh \
  && ${SCRIPTS_DIR}/start.sh
