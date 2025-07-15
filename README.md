# order-processor-gke

Project's File Structure
```
cloud-order-processor/
├── api/
│   ├── app.py                 # Flask app with /place-order endpoint
│   └── Dockerfile             # Container build file for API
│
├── worker/
│   ├── worker.py              # Pub/Sub message consumer
│   └── Dockerfile             # Container build file for Worker
│
├── k8s/
│   ├── deployment-api.yaml    # Deployment for the API service
│   ├── deployment-worker.yaml # Deployment for the Worker service
│   ├── service-api.yaml       # ClusterIP or LoadBalancer service for API
│   ├── ingress.yaml           # (Optional) Ingress + Load Balancer config
│   ├── configmap.yaml         # App environment config
│   └── hpa.yaml               # Horizontal Pod Autoscaler (optional)
│
├── pubsub/
│   └── pubsub-setup.sh        # Script to create topic + subscription
│
├── .dockerignore              # Ignore unnecessary files from Docker build
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Common Python deps (Flask, google-cloud-pubsub)
├── README.md                  # Project description and setup guide
└── architecture.png           # (Optional) Architecture diagram for GitHub

```

### Folder
```
/api/
Lightweight Flask API that accepts orders and publishes them to Pub/Sub.

JWT token validation simulated or stubbed (can be extended).

/worker/
Listens to the Pub/Sub subscription.

Logs or simulates order fulfillment.

/k8s/
Kubernetes manifests to deploy everything to GKE.

Includes optional autoscaling and Ingress configs.


/pubsub/
Shell script to create the Pub/Sub topic and subscription.

You can run this from Cloud Shell or locally with gcloud.

```
### PHASE 1 : SETUP THE ENVIRONMENT
I createad a GKE cluster called order-cluster. I used this option to take advantage of GKE's fully managed, serverless option for running Kubernetes workloads.

```
gcloud container clusters create-auto order-cluster --region=us-central1

```
