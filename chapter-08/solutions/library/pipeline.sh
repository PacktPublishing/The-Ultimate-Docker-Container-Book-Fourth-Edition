#! bin/bash

# Sample script to build, test and push a D
# containerized Java, SpringBoot and Gradle application.

# build the Docker image
docker image build -t $HUB_USER/$REPOSITORY:$TAG .
# Run all unit tests
docker container run --rm $HUB_USER/$REPOSITORY:$TAG gradle test
# Login to Docker Hub
docker login -u $HUB_USER -p $HUB_PWD
# Push the image to Docker Hub
docker image push $HUB_USER/$REPOSITORY:$TAG
