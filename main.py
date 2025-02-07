from flask import Flask, request, jsonify
import threading
import time
import logging

# Maximum number of concurrent requests
MAX_CONCURRENT_REQUESTS = 3
current_requests = 0

# Logging settings
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

#Creating a Flask application
app = Flask(__name__)

#Locks for concurrency management
t_lock = threading.Lock()

def load_shedding():
    """Checks if the number of concurrent requests has exceeded the limit"""
    global current_requests
    return current_requests > MAX_CONCURRENT_REQUESTS

@app.route('/')
def index():
    global current_requests
    
    with t_lock:
        current_requests += 1
        logging.info(f"Current requests before processing: {current_requests}")

    try:
        if load_shedding():
            status_code = 503  # Sending status code 503
            response = jsonify(message="Service Unavailable due to high load")
            response.status_code = status_code
            logging.info(f"Request to {request.url} returned status code {status_code}")
        else:
            # Simulation of heavy processing with 2 seconds delay
            time.sleep(2)  
            status_code = 200
            response = jsonify(message="Request processed successfully")
            response.status_code = status_code
    finally:
        with t_lock:
            current_requests -= 1
            logging.info(f"Current requests after processing: {current_requests}")
    
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
