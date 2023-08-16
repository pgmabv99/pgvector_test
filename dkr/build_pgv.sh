#!/bin/bash
. ./setup.sh
docker rm $cnt_phn --force 2>/dev/null || true
docker rmi $image_phn 2>/dev/null || true

util_copy
util_version

docker build -f dockerfile_phn \
             -t  $image_phn \
             --no-cache  \
             --build-arg cnt_user=$cnt_user \
             .

rm -r -f volume/*