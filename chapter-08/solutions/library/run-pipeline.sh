export HUB_USER=<your-docker-hub-username>
export HUB_PWD=<your-docker-hub-password>
export REPOSITORY=species-library
export TAG=latest

docker container run --rm \
    -e HUB_USER=$HUB_USER \
    -e HUB_PWD=$HUB_PWD \
    -e REPOSITORY=$REPOSITORY \
    -e TAG=$TAG \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd):/app \
    -w /app \
    docker:cli source pipeline.sh