from flask import Flask, jsonify
import threading
import time
import requests
import os 

SITE_URL = os.getenv("SITE_URL")

if SITE_URL is None:
    raise ValueError("SITE_URL environment variable is not set.")

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify(status="Running")

@app.route('/health')
def health():
    return jsonify(status="Healthy")

def ping_self():
    while True:
        try:
            res = requests.get(f"https://{SITE_URL}/health")
            if res.status_code != 200:
                print(f"Self ping failed with status code {res.status_code}")
            # else:
            #     print("Self ping succeeded")
        except Exception as e:
            print(f"Error in self-ping: {e}")
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=ping_self, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
