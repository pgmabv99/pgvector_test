# PG vector tests

https://github.com/pgvector/pgvector?ref=timescale.com#installation-notes

https://www.timescale.com/blog/postgresql-as-a-vector-database-create-store-and-query-openai-embeddings-with-pgvector/

Open AI

next actions
-minikube to run local image
-use pgvectot image
-wrap in python

-10/18
Ok -minikube  with pull from dockerhub
ok  - build local image + minikube image load  +  imagePullPolicy: Never
fail - build image inside minikube
takes 2 min to load image to minikube -known problem


minikube start
minikube ssh
minikube delete

kubectl apply -f dep.yaml


kubectl create secret generic regcred \
   --from-file=.dockerconfigjson=/home/pgmabv/.docker/config.json \
   --type=kubernetes.io/dockerconfigjson