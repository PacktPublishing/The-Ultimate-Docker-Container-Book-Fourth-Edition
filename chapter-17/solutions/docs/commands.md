# AWS EKS
Create the cluster:
```
eksctl create cluster \
    --name demo-cluster \
    --region eu-central-1 \
    --node-type t3.micro \
    --nodes 2 \
    --nodes-min 1 \
    --nodes-max 3 \
    --managed
```
Create the namespace:
```
kubectl create namespace taskboard
```
Configure kubectl to use the namespace in the current context
```
kubectl config set-context --current \
    --namespace=taskboard
```
Apply the configuration
```
```
Create secret
```
kubectl create secret generic taskboard-db-secret \
    --from-literal=POSTGRES_USER=taskuser \
    --from-literal=POSTGRES_PASSWORD=taskpass
```
Apply PostgreSQL
```
kubectl apply -f postgres.yaml
```
Verify that the database is up:
```
kubectl get pods -l app=postgres
kubectl get pvc
```
Apply the API:
```
kubectl apply -f api.yaml
```
and watch the rollout:
```
kubectl rollout status deployment/taskboard-api
kubectl get pods -l app=taskboard-api
```
Apply the Frontend:
```
kubectl apply -f frontend.yaml
```
check the external loadbalancer address
```
kubectl get svc taskboard-web
```


