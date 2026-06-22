# Kubernetes CrashLoopBackOff Investigation (Exercise 11)

## Objective

Investigate and resolve a `CrashLoopBackOff` issue for a Flask-based payment service running on Kubernetes.

---

## Project Structure

```
.
├── payment-deployment.yaml
├── payment-service.yaml
├── postgres-deployment.yaml
├── secret.yaml
├── app.py
├── Dockerfile
└── README.md
```

---

## Scenario

The payment application was repeatedly restarting with:

```
CrashLoopBackOff
```

The application depends on PostgreSQL.

---

## Investigation Steps

### 1. Check pod status

```bash
kubectl get pods
```

---

### 2. Describe failing pod

```bash
kubectl describe pod payment-deployment-xxxxx
```

Observed:

- Restart Count increasing
- Exit Code: 1

---

### 3. Check application logs

```bash
kubectl logs payment-deployment-xxxxx
```

---

### 4. Verify PostgreSQL

```bash
kubectl get pods
kubectl describe pod postgres-deployment-xxxxx
```

Found PostgreSQL was initially unavailable while the image was being pulled.

---

## Root Cause

The application attempted to connect using an incorrect database host.

Incorrect:

```
DB_HOST=<old value>
```

Correct:

```
DB_HOST=postgres-service
```

Additionally, the application had no startup probe, so Kubernetes restarted it before PostgreSQL was ready.

---

## Fixes

- Created PostgreSQL Deployment
- Created PostgreSQL Service
- Updated Kubernetes Secret
- Added Startup Probe
- Added Liveness Probe
- Restarted Deployment

---

## Validation

```
kubectl get pods
```

Output:

```
payment-deployment   1/1 Running
postgres-deployment  1/1 Running
```

---

## Kubernetes Commands Used

```bash
kubectl get pods
kubectl describe pod payment-deployment
kubectl logs payment-deployment
kubectl rollout restart deployment payment-deployment
kubectl get svc
```

---

## Lessons Learned

- Always use Kubernetes Service DNS instead of Pod IPs.
- Configure startup probes for applications that depend on databases.
- Use `kubectl describe` and `kubectl logs` for CrashLoopBackOff debugging.
- Verify dependencies are healthy before restarting dependent workloads.
