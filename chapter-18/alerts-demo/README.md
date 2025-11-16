# 🧭 OpenTelemetry Demo – Orders & Payments on Kubernetes

This demo shows how to instrument, deploy, and visualize distributed traces for a simple microservices application running on **Kubernetes**.  
It includes:

- **orders-service** (Python / Flask)  
- **payments-service** (Node.js / Express)  
- **OpenTelemetry Collector**  
- **Jaeger All-in-One** for trace visualization  

All components run inside the **observability** namespace on your **minikube** cluster.

---

## 🏗️ 1. Prerequisites

Before you begin, make sure you have:

- [kubectl](https://kubernetes.io/docs/tasks/tools/)  
- [minikube](https://minikube.sigs.k8s.io/docs/start/)  
- [Docker](https://docs.docker.com/get-docker/)  

Start your cluster:

```bash
minikube start
```

(Optional) use the observability namespace by default:

```bash
kubectl create namespace observability
kubectl config set-context --current --namespace=observability
```

---

## 🧱 2. Build and push images

From the project root (where the `python-orders` and `node-payments` folders are):

```bash
# Build Python orders service
docker build -t orders-service:otel ./python-orders

# Build Node payments service
docker build -t payments-service:otel ./node-payments
```

If you’re using minikube’s internal Docker registry:

```bash
eval $(minikube docker-env)
```

Then re-run the build commands above (no need to push to an external registry).

---

## 🚀 3. Deploy the stack

Apply all manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/jaeger-all-in-one.yaml
kubectl apply -f k8s/otel-collector.yaml
kubectl apply -f k8s/payments-deployment.yaml
kubectl apply -f k8s/orders-deployment.yaml
```

Check everything is running:

```bash
kubectl get pods
```

Expected output:

```
NAME                                 READY   STATUS    RESTARTS   AGE
jaeger-xxxxxx                        1/1     Running   0          1m
otel-collector-xxxxxx                1/1     Running   0          1m
orders-service-xxxxxx                1/1     Running   0          1m
payments-service-xxxxxx              1/1     Running   0          1m
```

---

## 📡 4. Generate traces

Port-forward the **orders-service** and send some requests:

```bash
kubectl port-forward svc/orders-service 18080:8080
```

Then run:

```bash
for i in $(seq 1 10); do
  curl -s -X POST http://localhost:18080/order     -H "Content-Type: application/json"     -d "{\"orderId\":\"demo-$i\"}" >/dev/null
  sleep 0.3
done
```

The `orders-service` will call the `payments-service`, creating distributed traces.

---

## 🔍 5. View traces in Jaeger

Port-forward the **Jaeger UI**:

```bash
kubectl port-forward svc/jaeger-query 16686:16686
```

Open your browser at:

👉 [http://localhost:16686](http://localhost:16686)

Select **orders-service** from the *Service* dropdown and click **Find Traces**.

You’ll see end-to-end traces showing:

```
orders-service → payments-service
```

with spans and latency data for each request.

---

## 🧩 6. Verify Collector and Jaeger logs

Check that your pipeline is healthy:

```bash
kubectl logs deploy/otel-collector
kubectl logs deploy/jaeger
```

Expected messages include:

```
Everything is ready. Begin running and processing data.
Starting HTTP server {"endpoint": "0.0.0.0:4318"}
Starting jaeger-collector gRPC server {"grpc.host-port": "[::]:14250"}
```

---

## 🧼 7. Clean up

To remove everything:

```bash
kubectl delete namespace observability
```

Or, if you only used this demo:

```bash
minikube delete
```

---

## 🧠 Summary

You now have a complete OpenTelemetry tracing pipeline running on Kubernetes:
```
orders-service → payments-service → OpenTelemetry Collector → Jaeger
```

From here, you can extend the setup with:
- **Prometheus & Grafana** for metrics  
- **Alertmanager** for alerting  
- **Argo CD** for GitOps and drift detection  

This foundation prepares you for the next chapter:  
➡️ *Collecting and Visualizing Metrics with Prometheus and Grafana.*
