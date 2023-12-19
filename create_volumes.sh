#!/bin/bash

function create_volumes() {
  dirs=("$@")
  for i in "${dirs[@]}"; do
    mkdir -p $i
  done
}

VOLUME_PATH=~/homelab-containers

docker_volumes=("${VOLUME_PATH}/portainer/portainer_data" "${VOLUME_PATH}/nginx/nginx_data" "${VOLUME_PATH}/nginx/nginx_db" "${VOLUME_PATH}/nginx/nginx_certs" "${VOLUME_PATH}/dashy/icons" "${VOLUME_PATH}/jenkins/data" "${VOLUME_PATH}/jenkins/certs")

create_volumes "${docker_volumes[@]}"

rsync -r ./dashy $VOLUME_PATH/

# TODO: Setup dynamic device scannig and crating appropriate dirs.
# TODO: Add cleaning mechanism.
# TODO: And first setup also. Don't foreget to backup volumes and restore them.