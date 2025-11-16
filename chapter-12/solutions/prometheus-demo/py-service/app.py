from flask import Flask
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
import logging, sys

app = Flask(__name__)

# Enable unbuffered logging to stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Define a simple counter
counter = Counter('py_requests_total',
                  'Total HTTP requests handled')

@app.route('/')
def home():
    counter.inc()
    app.logger.info("Handled request to /")
    return 'Hello from Python!'

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {
      'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.logger.info("Starting Flask app on port 8082")
    app.run(host='0.0.0.0', port=8082)
