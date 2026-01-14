# Black Coordinates List

Two-service FastAPI system:

- **Service A**: Receives an IP address, queries an external GeoIP API to resolve coordinates, then forwards the result to Service B.
- **Service B**: Validates and stores `{ip, lat, lon}` in **Redis (Key-Value)** and exposes an endpoint to retrieve all stored entries.

## Architecture (End-to-End)

1. Client -> **Service A**: `POST /resolve-ip` with `{ "ip": "x.x.x.x" }`
2. **Service A** -> External GeoIP provider: gets `{lat, lon}`
3. **Service A** -> **Service B**: `POST /coordinates` with `{ip, lat, lon}`
4. **Service B** -> **Redis**: stores under key `coord:{ip}`
5. Client -> **Service B**: `GET /coordinates` returns the stored list

> Service A does **not** talk to Redis directly.

## Run with Docker Compose

From the project root:

```bash
docker compose up --build
```

Ports:
- Service A: http://localhost:8001
- Service B: http://localhost:8002
- Redis: localhost:6379

### Quick test

Resolve + store:

```bash
curl -X POST http://localhost:8001/resolve-ip   -H "Content-Type: application/json"   -d '{"ip":"8.8.8.8"}'
```

List stored coordinates (from Service B):

```bash
curl http://localhost:8002/coordinates
```

Health:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
```

## Environment variables

Copy `.env.example` into your environment (Compose already sets needed vars):

- `SERVICE_B_URL` (Service A) — e.g. `http://service-b:8000`
- `EXTERNAL_GEOIP_URL` (Service A) — base URL, called as `{base}/{ip}`
- `REDIS_HOST`, `REDIS_PORT` (Service B)

## Kubernetes (Minikube)

Manifests are in `k8s/`:
- Redis StatefulSet + PVC
- Service A Deployment + Service
- Service B Deployment + Service

Apply:

```bash
kubectl apply -f k8s/
```

Expose Service A locally (example):

```bash
kubectl port-forward svc/service-a 8001:8000
```

Then call Service A on `http://localhost:8001`.
