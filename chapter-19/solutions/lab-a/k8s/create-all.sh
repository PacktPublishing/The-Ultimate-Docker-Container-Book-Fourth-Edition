#!/bin/sh
set -e

kubectl apply -f demo-namespace.yaml -n aiops
kubectl apply -f demo-autoscaler.yaml -n aiops
kubectl apply -f demo-service-account.yaml -n aiops
kubectl apply -f demo-rbac.yaml -n aiops
kubectl apply -f demo-deployment.yaml -n aiops
kubectl apply -f demo-cronjob.yaml -n aiops
