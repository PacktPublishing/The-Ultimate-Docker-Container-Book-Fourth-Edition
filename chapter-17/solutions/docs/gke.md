# Preparing an Azure Account for the exercise
## Account creation
* Create a free account here: https://cloud.google.com/free


## Install Google Cloud CLI
```
brew update
brew install --cask gcloud-cli
gcloud version
```
If you have gcloud already installed but your version is not at least 420 then update it
```
gcloud update
```
Install the auth plugin
```
gcloud components install gke-gcloud-auth-plugin
```

# Authenticate and start
```
gcloud auth login
gcloud projects create taskboard-demo-project \
    --name="TaskBoard Demo"
gcloud config set project taskboard-demo-project
gcloud services enable container.googleapis.com \
    compute.googleapis.com
gcloud config set compute/region europe-west3
gcloud config set compute/zone europe-west3-a
```
# Create the cluster
```
gcloud container clusters create taskboard-gke \
  --zone europe-west3-a \
  --num-nodes 2 \
  --machine-type e2-small
```