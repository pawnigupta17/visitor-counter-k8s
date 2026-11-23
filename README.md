# Visitor Counter Web Application – Hybrid Cloud Simulation

## 1. Project Overview
This project demonstrates a scalable Visitor Counter Web Application using Flask, Redis, Docker, Docker Compose and Kubernetes.

The application counts website visits, stores the count in Redis and displays the visitor count and cluster name.

## 2. Technologies Used
- Python and Flask
- Redis
- Docker and Docker Compose
- Kubernetes and Minikube
- Horizontal Pod Autoscaler (HPA)
- Ubuntu WSL2

## 3. Architecture
User → Flask Web Application → Redis Database

Docker Compose is used for local deployment. Kubernetes manages application deployments, services, health checks and automatic scaling.

Two separate Minikube clusters simulate a hybrid-cloud environment:
- Private Cloud: Primary cluster
- Public Cloud: Secondary cluster

## 4. Project Features
- Visitor counting using Redis.
- Persistent visitor count.
- Docker containerization.
- Kubernetes deployments and services.
- Readiness and liveness probes.
- Automatic pod recovery.
- CPU and memory resource requests and limits.
- Horizontal Pod Autoscaling.
- Hybrid-cloud failover simulation.

## 5. Docker Setup

Build and start the application:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

Stop the application:

```bash
docker compose down
```

## 6. Kubernetes Deployment

Build the application image:

```bash
minikube -p private-cloud image build -t visitor-counter:v1 .
```

Apply Kubernetes configurations:

```bash
kubectl apply -f k8s/
```

Check resources:

```bash
kubectl get pods,deploy,svc,hpa
```

## 7. Autoscaling

The Horizontal Pod Autoscaler is configured with:
- Minimum replicas: 2
- Maximum replicas: 6
- Target CPU utilization: 50%

During load testing, the application scaled from 2 to 6 replicas and returned to 2 replicas after the load was removed.

## 8. Hybrid Cloud Simulation

Two independent Minikube clusters were created to simulate private and public cloud environments.

The same application was deployed on both clusters.

For the failover demonstration:
1. The private-cloud cluster was stopped.
2. The public-cloud application remained accessible.
3. The private-cloud cluster was restarted afterward.

Note: This is a local hybrid-cloud simulation using Minikube, not a deployment on actual public and private cloud providers. Failover was demonstrated manually.

## 9. Cost Optimization

The project demonstrates three resource optimization techniques:

1. Docker image optimization: Uses the Python slim base image, disables pip cache and avoids unnecessary bytecode files.
2. Resource right-sizing: Web containers use CPU requests of 100m and memory requests of 64Mi, with limits of 250m CPU and 128Mi memory.
3. Horizontal autoscaling: Maintains 2 replicas during low load and scales up to 6 replicas when CPU utilization increases.

### Docker Image Size Measurement

Both the baseline and current Dockerfiles were built and measured using Docker Desktop.

| Measurement | Baseline | Current |
|---|---:|---:|
| Disk usage | 191 MB | 191 MB |
| Content size | 46.1 MB | 46.1 MB |
| Exact image size | 46,138,672 bytes | 46,138,672 bytes |

Measured image size reduction: 0%.

The comparison showed no additional image size reduction because the baseline already used the same Docker optimization practices.

### Observed Resource Usage

- Web pod CPU: approximately 1m each.
- Web pod memory: approximately 63–65Mi each.
- Redis memory: approximately 9Mi.

These measurements demonstrate resource management and autoscaling. Actual monetary savings depend on the cloud provider and pricing model.

## 10. Health Check Endpoints
- `/health` – Liveness check.
- `/ready` – Readiness check.
- `/api/visits` – Visitor count API.

## 11. Screenshots

Project demonstration screenshots are available in the `screenshots/` directory.

## 12. Conclusion

This project demonstrates containerization, orchestration, monitoring, autoscaling, resource optimization and hybrid-cloud failover concepts through a practical Visitor Counter Web Application.
