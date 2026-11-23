# Visitor Counter Web Application -- Hybrid Cloud Simulation

## 1. Project Overview

This project demonstrates a scalable Visitor Counter Web Application
using Flask, Redis, Docker, Docker Compose and Kubernetes.

The application counts website visits, stores the count in Redis and
displays the visitor count and cluster name.

## 2. Technologies Used

-   Python and Flask
-   Redis
-   Docker and Docker Compose
-   Kubernetes and Minikube
-   Horizontal Pod Autoscaler (HPA)
-   Ubuntu WSL2

## 3. Architecture

**User → Flask Web Application → Redis Database**

Docker Compose is used for local deployment. Kubernetes manages
application deployments, services, health checks and automatic scaling.

Two separate Minikube clusters simulate a hybrid-cloud environment:

-   **Private Cloud:** Primary cluster
-   **Public Cloud:** Secondary cluster

Refer to `architecture/architecture-diagram.png` for the architecture
diagram.

## 4. Project Features

-   Visitor counting using Redis.
-   Persistent visitor count.
-   Docker containerization.
-   Kubernetes deployments and services.
-   Readiness and liveness probes.
-   Automatic pod recovery.
-   CPU and memory resource requests and limits.
-   Horizontal Pod Autoscaling.
-   Hybrid-cloud failover simulation.

## 5. Docker Setup

Build and start the application:

``` bash
docker compose up -d --build
```

Check running containers:

``` bash
docker compose ps
```

Stop the application:

``` bash
docker compose down
```

## 6. Kubernetes Deployment

Run the following commands from the project directory in Ubuntu WSL2.
Select the cluster you want to deploy to.

Build the application image for the private cluster:

``` bash
minikube -p private-cloud image build -t visitor-counter:v1 .
```

Select the private cluster:

``` bash
kubectl config use-context private-cloud
```

Apply the Kubernetes YAML files stored in the `docs/` directory:

``` bash
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/web.yaml
kubectl apply -f k8s/hpa.yaml
```

Check resources:

``` bash
kubectl get pods,deploy,svc,hpa
```

For the public cluster, build the image into that Minikube profile and
repeat the deployment using the `public-cloud` context:

``` bash
minikube -p public-cloud image build -t visitor-counter:v1 .
kubectl config use-context public-cloud
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/web.yaml
kubectl apply -f k8s/hpa.yaml
```

## 7. Autoscaling

The Horizontal Pod Autoscaler is configured with:

-   **Minimum replicas:** 2
-   **Maximum replicas:** 6
-   **Target CPU utilization:** 50%

During load testing, the application scaled from 2 to 6 replicas and
returned to 2 replicas after the load was removed.

## 8. Hybrid Cloud Simulation

Two independent Minikube clusters were created to simulate private and
public cloud environments.

The same application was deployed on both clusters.

For the failover demonstration:

1.  The private-cloud cluster was stopped.
2.  The public-cloud application remained accessible.
3.  The private-cloud cluster was restarted afterward.

**Note:** This is a local hybrid-cloud simulation using Minikube, not a
deployment on actual public and private cloud providers. Failover was
demonstrated manually.

## 9. Cost Optimization

The project demonstrates three resource optimization techniques:

1.  **Docker image optimization:** Uses a Python slim base image and pip
    installation without retaining the package cache.
2.  **Resource right-sizing:** Web containers use CPU requests of 100m
    and memory requests of 64Mi, with limits of 250m CPU and 128Mi
    memory.
3.  **Horizontal autoscaling:** Maintains 2 replicas during low load and
    scales up to 6 replicas when CPU utilization increases.

### 9.1 Docker Image Size Comparison

A controlled comparison was performed between a deliberately unoptimized
Docker build and the current optimized project build.

  Measurement           Unoptimized comparison build     Current optimized build
  ------------------ ------------------------------- ---------------------------
  Image                `visitor-counter:unoptimized`   `visitor-counter:current`
  Exact image size                 419,941,666 bytes            46,138,672 bytes
  Approximate size                            420 MB                     46.1 MB

**Measured reduction: 89.01%.**

The unoptimized comparison build used the full `python:3.12` base image,
copied the complete project directory and installed dependencies without
disabling pip's cache.

The current project build uses the optimized Dockerfile.

**Historical baseline note:** The earlier baseline and current optimized
image were both measured at 46,138,672 bytes, showing 0% difference
between those two builds. The 89.01% result is from a separate
controlled comparison build, not a historical measurement.

See `docs/Dockerfile.unoptimized` and `docs/docker-image-comparison.txt`
for the comparison details.

### 9.2 Kubernetes Resource Right-Sizing

The current web deployment uses the following resource configuration:

  Resource     Request per pod   Limit per pod
  ---------- ----------------- ---------------
  CPU                     100m            250m
  Memory                  64Mi           128Mi

The final observed snapshot showed:

-   Web pod CPU usage: approximately 1m per pod.
-   Web pod memory usage: approximately 63--65Mi per pod.
-   Combined web pod CPU usage: 2m.
-   Combined web pod memory usage: 128Mi.

These are measured usage values compared with configured resource
requests and limits. They are not a before-and-after measurement of an
older deployment.

### 9.3 Horizontal Pod Autoscaling Resource Comparison

The HPA was configured with a minimum of 2 replicas and a maximum of 6
replicas.

  Configuration                    CPU requests   Memory requests
  ------------------------------ -------------- -----------------
  Fixed 6 replicas                         600m             384Mi
  HPA at 2 replicas (low load)             200m             128Mi

The calculated reduction in requested resources at low load is 66.7%
compared with keeping 6 replicas running continuously.

The actual scaling from 2 to 6 replicas and back to 2 was demonstrated
during load testing.

This is a calculated comparison of configured resource requests, not
measured cloud-billing savings.

### 9.4 Cost Optimization Summary

The measurements demonstrate Docker image size reduction, Kubernetes
resource monitoring and HPA-based scaling.

All figures represent image sizes, resource usage or configured resource
requests. No actual cloud billing data or monetary savings are claimed
because the project uses a local Minikube environment.

For the complete comparison table and measurement notes, refer to
`docs/cost-analysis.md`.

## 10. Health Check Endpoints

-   `/health` -- Liveness check.
-   `/ready` -- Readiness check.
-   `/api/visits` -- Visitor count API.

## 11. Screenshots and Documentation

Project demonstration screenshots are available in the `screenshots/`
directory.

Additional project documentation:

-   `architecture/architecture-diagram.png` -- Project architecture
    diagram.
-   `docs/cost-analysis.md` -- Cost optimization comparison.
-   `docs/docker-image-comparison.txt` -- Docker image measurements.
-   `github_link.txt` -- GitHub repository link.

## 12. Conclusion

This project demonstrates containerization, orchestration, monitoring,
autoscaling, resource optimization and hybrid-cloud failover concepts
through a practical Visitor Counter Web Application.
