#!/bin/sh
set -e

kubectl delete -f demo-cronjob.yaml -n aiops --ignore-not-found
kubectl delete -f demo-deployment.yaml -n aiops --ignore-not-found
kubectl delete -f demo-service-account.yaml -n aiops --ignore-not-found
kubectl delete -f demo-rbac.yaml -n aiops --ignore-not-found
kubectl delete -f demo-autoscaler.yaml -n aiops --ignore-not-found
kubectl delete -f demo-namespace.yaml -n aiops --ignore-not-found
