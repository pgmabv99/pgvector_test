#!/bin/bash
. ./setup.sh
docker stop  $cnt_dep
docker rm $cnt_dep

docker volume rm  postgres_data 2>/dev/null || true
docker volume create postgres_data
docker run -d  \
    --name  $cnt_dep \
    -e POSTGRES_PASSWORD=pass1 \
    -p 5432:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    $image_dep

docker exec -it $cnt_dep /bin/bash