import threading, time
from flask import request, jsonify
from flask_login import login_required
from flask import Flask
from config import Config
import logging

app = Flask(__name__)

# Auto-scaling parameters
TARGET_CPU = Config.TARGET_CPU
SLEEP_INTERVAL = Config.SLEEP_INTERVAL
MAX_REPLICAS_CHANGE = Config.MAX_REPLICAS_CHANGE

# Configure logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


class AutoScaler:
    def __init__(self):
        self.cpu_utilization = 0.5
        self.replicas = 1
        self.replicas_lock = threading.Lock()


auto_scaler = AutoScaler()


# Auto-scaling logic
def auto_scale():
    global auto_scaler

    while True:
        auto_scaler.cpu_utilization += 0.05

        if auto_scaler.cpu_utilization > TARGET_CPU:
            with auto_scaler.replicas_lock:
                auto_scaler.replicas = max(1, auto_scaler.replicas - 1)
        else:
            with auto_scaler.replicas_lock:
                auto_scaler.replicas += 1

        log.debug(f"Auto-scaling: CPU={auto_scaler.cpu_utilization:.2f}, Replicas={auto_scaler.replicas}")
        time.sleep(SLEEP_INTERVAL)


class ScaleService:

    @app.route('/app/status', methods=['GET'])
    @login_required
    def get_status(self):
        return jsonify({"cpu": {"highPriority": auto_scaler.cpu_utilization}, "replicas": auto_scaler.replicas})

    @app.route('/app/replicas', methods=['PUT'])
    @login_required
    def update_replicas(self):
        try:
            data = request.get_json()
            new_replicas = data.get('replicas', None)
            trigger_person = data.get('trigger_person', None)

            if new_replicas is None or not isinstance(new_replicas, int) or new_replicas < 1:
                return jsonify({"error": "Invalid replica count"}), 400

            with auto_scaler.replicas_lock:
                if abs(new_replicas - auto_scaler.replicas) > MAX_REPLICAS_CHANGE:
                    if trigger_person is None:
                        return jsonify(
                            {"error": "Trigger person is required for changes greater than 50 replicas"}), 400

                auto_scaler.replicas = new_replicas

            return jsonify({"message": f"Replica count updated to {auto_scaler.replicas} by {trigger_person}"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
