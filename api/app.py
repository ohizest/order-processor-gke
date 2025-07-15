from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import os
import json

app = Flask(__name__)

# Environment variables
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "order-topic")

# Initialize Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

# Simulated JWT validation
def validate_jwt(token):
    if token == "dummy-token":
        return True
    return False

@app.route('/place-order', methods=['POST'])
def place_order():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if not validate_jwt(token):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        order_data = request.get_json()
        message_json = json.dumps(order_data).encode("utf-8")
        future = publisher.publish(topic_path, data=message_json)
        future.result()  # Block until published
        return jsonify({"message": "Order received and published to Pub/Sub"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Order API is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
