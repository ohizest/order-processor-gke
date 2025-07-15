from google.cloud import pubsub_v1
import os
import json
import time

# Environment variables
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
SUBSCRIPTION_ID = os.getenv("PUBSUB_SUB_ID", "order-sub")

# Full subscription path
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# Callback function to process messages
def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        print(f" Received order: {data}")
        message.ack()
    except Exception as e:
        print(f" Error processing message: {e}")
        message.nack()

# Subscribe and listen
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f" Listening for messages on {subscription_path}...\n")

# Keep the main thread alive
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print(" Worker stopped.")
