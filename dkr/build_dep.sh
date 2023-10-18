#!/bin/bash
. ./setup.sh
docker stop --time 0 $cnt_dep
docker rm $cnt_dep
docker rmi $image_dep
docker build -f dockerfile_dep \
    --no-cache \
    -t $image_dep \
    --build-arg cnt_user=$cnt_user \
    .
# minikube image build -f dockerfile_dep \
#     -t pgmabv99/dep \
#     .
