#!/bin/sh
set -e

kubectl delete -f k8s/demo-cronjob.yaml -n aiops --ignore-not-found
kubectl delete -f k8s/demo-deployment.yaml -n aiops --ignore-not-found
kubectl delete -f k8s/demo-service-account.yaml -n aiops --ignore-not-found
kubectl delete -f k8s/demo-rbac.yaml -n aiops --ignore-not-found
kubectl delete -f k8s/demo-autoscaler.yaml -n aiops --ignore-not-found
kubectl delete -f k8s/demo-namespace.yaml -n aiops --ignore-not-found