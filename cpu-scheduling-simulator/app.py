"""
Flask Web Application for CPU Scheduling Mini Project.
Provides endpoints for Queue & Priority Queue Scheduling.
"""

import os
import zipfile
from flask import Flask, render_template, request, jsonify, send_file
from scheduler import run_queue_scheduling, run_priority_queue_scheduling

app = Flask(__name__)

# Default minimal sample workload
DEFAULT_PROCESSES = [
    {"pid": "P1", "arrival_time": 0, "burst_time": 4, "priority": 3, "color": "#3b82f6"},
    {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1, "color": "#10b981"},
    {"pid": "P3", "arrival_time": 2, "burst_time": 1, "priority": 4, "color": "#f59e0b"},
    {"pid": "P4", "arrival_time": 3, "burst_time": 2, "priority": 2, "color": "#ec4899"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/default-processes", methods=["GET"])
def get_default_processes():
    return jsonify(DEFAULT_PROCESSES)

@app.route("/api/simulate", methods=["POST"])
def simulate():
    try:
        data = request.get_json(force=True)
        mode = data.get("mode", "queue").lower()
        processes = data.get("processes", [])

        if not processes:
            return jsonify({"error": "Process list cannot be empty."}), 400

        if mode == "priority_queue":
            result = run_priority_queue_scheduling(processes)
        else:
            result = run_queue_scheduling(processes)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download-project", methods=["GET"])
def download_project():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        zip_path = os.path.join(base_dir, "..", "cpu-scheduling-simulator.zip")
        zip_path = os.path.abspath(zip_path)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(base_dir):
                # Ignore __pycache__ and git folders
                dirs[:] = [d for d in dirs if d != '__pycache__' and not d.startswith('.')]
                for file in files:
                    if file.endswith('.pyc') or file.startswith('.'):
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=os.path.dirname(base_dir))
                    zipf.write(file_path, arcname)

        return send_file(
            zip_path,
            as_attachment=True,
            download_name="cpu-scheduling-simulator.zip",
            mimetype="application/zip"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
