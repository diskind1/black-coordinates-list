# Kubernetes (Minikube)

These manifests expect local images:

- ipcoords-service-a:latest
- ipcoords-service-b:latest

Build inside Minikube Docker (example):

```bash
minikube start
minikube docker-env | Invoke-Expression   # PowerShell
docker build -t ipcoords-service-b:latest -f service-b/app/Dockerfile service-b
docker build -t ipcoords-service-a:latest -f service-a/app/Dockerfile service-a
kubectl apply -f k8s/
```

Port-forward Service A:

```bash
kubectl port-forward svc/service-a 8001:8000
```
