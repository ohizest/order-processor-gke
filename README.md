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
Next I configured the api.py, the dockerfile and the requirements.txt

Next is to test the Flask App on my local machine before containerizing it.

```
cd order-processor-gke/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Setting environment variables. This passes the configuration into app.py without hardcoding my GCP project id directly in the code.

The image below confirms the order API is running locally. 

Next I used ```curl``` to simulate placing an order. ```curl``` lets me send HTTP requests directly to my Order API.

I get ```{"error":"404 Resource not found (resource=order-topic)."}``` from the Google Pub/Sub Python client, which is trying to publish to a topic named order-topic, but the topic hasn’t been created at this stage in this project even though this is confirmation that the order API is running locally.

After configuring the worker.py, we create a subscription named order-sub that will listen to the order-topic.

Testing locally was successful. The data workflow: 

Here’s how a typical order flows through this system:

* Client → Flask API:

Sends an HTTP request with order data (e.g., { "order_id": 123, "items": [...] }).

*Flask API → Pub/Sub:

Publishes the order as a message to order-topic.

* Pub/Sub → Python Worker:

The worker pulls the message from order-sub.

Python Worker:

Processes the order (e.g., saves to DB, sends confirmation).

Acknowledges the message (removes it from Pub/Sub).


Next is to configure the dockerfiles for the Flask API and for Pub/Sub Worker

Next build the docker image for the worker and api directory using Cloud Build & Push.

From your api directory:

```
gcloud builds submit --tag gcr.io/order-processing-microservice/order-api .
```

From your worker directory:
```
gcloud builds submit --tag gcr.io/order-processing-microservice/order-worker .
```