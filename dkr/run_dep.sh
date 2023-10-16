#!/bin/bash
. ./setup.sh
set -x
docker kill  $cnt_dep
docker rm $cnt_dep

docker volume rm  postgres_data 2>/dev/null || true
docker volume create postgres_data
docker run -d  \
    --name  $cnt_dep \
    -e POSTGRES_PASSWORD=pass1 \
    -e OPEN_API_KEY=$OPEN_API_KEY \
    -p 5432:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    --mount type=bind,source=$git_root,target=/postgres/pgvector_test \
    --mount type=bind,source=$git_root/../tmp_pgv,target=/postgres/tmp_pgv \
    $image_dep


docker exec -it $cnt_dep pg_init
docker exec -it $cnt_dep pg_start
docker exec -it $cnt_dep psql -c "CREATE EXTENSION vector"

docker exec -it $cnt_dep /bin/bash