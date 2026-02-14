# Lior Beauty Store – Kubernetes Microservices App

Welcome to **Lior Beauty Store**, a simple microservices-based demo application running on a **Kubernetes (k8s) cluster**.

This project is designed to demonstrate how a real-world store application can be split into multiple services:

- Frontend service (HTML UI)
- Backend services (Catalog, Payments, Auth)
- Database service (DB)

---

## 🏗 Architecture Overview

The system looks like this:

```
User --> Frontend --> Backend Services --> Database
```

### Services inside the cluster

| Component   | Description |
|------------|-------------|
| **Frontend** | Web UI service (HTML + Python service) |
| **Backend**  | Microservices: Catalog, Payments, Authentication |
| **Database** | Stores application data |
| **User**     | External client accessing the app |

---

## 📦 Microservices Breakdown

### 1. Frontend Service

The frontend is responsible for:

- Serving the HTML UI
- Sending requests to backend APIs

Includes:

- `service.py`
- `requirements.txt`
- `Dockerfile`

---

### 2. Backend Services

Backend is split into multiple microservices:

- **Catalog Service** – Product listings
- **Payments Service** – Payment processing
- **Auth Service** – Login & authentication

Each backend service contains:

- `service.py`
- `requirements.txt`
- `Dockerfile`

---

### 3. Database (DB)

The database runs as its own containerized service.

- Persistent storage recommended using PVC
- Connected internally only inside the cluster

---

## 🚀 Deployment on Kubernetes

### Prerequisites

Make sure you have:

- Kubernetes cluster running
- `kubectl`
- Docker
- Helm (optional)

---

### Step 1: Build Docker Images

Example:

```bash
docker build -t your-dockerhub/frontend:latest ./frontend
docker build -t your-dockerhub/catalog:latest ./backend/catalog
docker build -t your-dockerhub/payments:latest ./backend/payments
docker build -t your-dockerhub/auth:latest ./backend/auth
```

Push them:

```bash
docker push your-dockerhub/frontend:latest
...
```

---

### Step 2: Deploy to Kubernetes

Apply manifests:

```bash
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/db.yaml
```

---

### Step 3: Access the App

If using Ingress:

```bash
kubectl get ingress
```

Or port-forward frontend:

```bash
kubectl port-forward svc/frontend 8080:80
```

Then open:

```
http://localhost:8080
```

---

## 📊 Observability (Optional)

You can extend this project with:

- Prometheus metrics
- Grafana dashboards
- HPA autoscaling

---

## 🔥 Future Improvements

- Add CI/CD pipeline with Jenkins or GitHub Actions
- Use Helm charts for full deployment
- Add persistent volumes for DB
- Add Service Mesh (Istio)

---

## 👨‍💻 Author

Built as a DevOps learning project to understand:

- Microservices vs Monolith
- Kubernetes networking & service discovery
- CI/CD automation
- Cloud-native architecture

Enjoy 🚀
