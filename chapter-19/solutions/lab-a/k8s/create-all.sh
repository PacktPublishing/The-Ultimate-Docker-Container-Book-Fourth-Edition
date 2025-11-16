#!/bin/sh
set -e

kubectl apply -f k8s/demo-namespace.yaml -n aiops
kubectl apply -f k8s/demo-autoscaler.yaml -n aiops
kubectl apply -f k8s/demo-service-account.yaml -n aiops
kubectl apply -f k8s/demo-rbac.yaml -n aiops
kubectl apply -f k8s/demo-deployment.yaml -n aiops
kubectl apply -f k8s/demo-cronjob.yaml -n aiops