from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server
import time

app = Flask(__name__)

# Define a Counter metric for HTTP requests
http_requests_total = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

@app.route('/')
def home():
    http_requests_total.labels(method='GET', endpoint='/').inc()
    return "Hello welcome to Mohamed's Kubernetes project Flask!"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # Optionally start Prometheus server on a different port if needed
    # start_http_server(8000)
    app.run(host='0.0.0.0', port=8000)
