import os
import uuid
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for

LITELLM_ADMIN_URL = os.getenv("LITELLM_ADMIN_URL", "http://litellm:4000")
LITELLM_ADMIN_KEY = os.getenv("LITELLM_ADMIN_KEY", "changeme")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/create_key", methods=["POST"])
def create_key():
    data = request.json or {}
    student_name = data.get("student_name", "student")
    package = data.get("package", "basic")

    # Example payload; adjust according to LiteLLM admin API spec
    payload = {
        "metadata": {"student_name": student_name, "package": package},
        "budget": 5.0,  # $5 default
        "models": ["gpt-4o-mini"],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LITELLM_ADMIN_KEY}"
    }

    try:
        resp = requests.post(
            f"{LITELLM_ADMIN_URL}/key/generate",
            json=payload,
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        key_data = resp.json()
        virtual_key = key_data.get("key", str(uuid.uuid4()))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"virtual_key": virtual_key})


@app.route("/api/list_keys", methods=["GET"])
def list_keys():
    """列出所有虛擬金鑰 (簡易封裝)"""
    headers = {
        "Authorization": f"Bearer {LITELLM_ADMIN_KEY}"
    }
    try:
        resp = requests.get(f"{LITELLM_ADMIN_URL}/key/list", headers=headers, timeout=15)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/delete_key/<key_id>", methods=["DELETE"])
def delete_key(key_id):
    """刪除指定金鑰"""
    headers = {
        "Authorization": f"Bearer {LITELLM_ADMIN_KEY}"
    }
    try:
        resp = requests.delete(f"{LITELLM_ADMIN_URL}/key/delete/{key_id}", headers=headers, timeout=15)
        resp.raise_for_status()
        return jsonify({"status": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
