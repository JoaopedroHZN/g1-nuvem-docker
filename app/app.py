import os
import json
import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Variáveis injetadas pelo Docker Compose
APP_NAME = os.environ.get('APP_NAME', 'app_default')
PEERS = os.environ.get('PEERS', '').split(',')
SHARED_DIR = '/data'
MESSAGES_FILE = os.path.join(SHARED_DIR, 'messages.json')
LOG_FILE = os.path.join(SHARED_DIR, f'{APP_NAME}.log')

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def save_message(message_data):
    messages = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r') as f:
                messages = json.load(f)
        except json.JSONDecodeError:
            pass
    messages.append(message_data)
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    if not data:
        return jsonify({"error": "JSON invalido"}), 400

    logging.info(f"Mensagem recebida: {data}")
    is_forwarded = request.headers.get('X-Forwarded') == 'true'

    if not is_forwarded:
        save_message(data)
        for peer in PEERS:
            if peer:
                try:
                    url = f"http://{peer}:5000/send"
                    requests.post(url, json=data, headers={'X-Forwarded': 'true'}, timeout=2)
                    logging.info(f"Replicado para {peer}")
                except Exception as e:
                    logging.error(f"Falha ao replicar para {peer}: {e}")
        return jsonify({"status": "Mensagem guardada e replicada", "data": data}), 201
    else:
        return jsonify({"status": "Copia recebida e registada no log"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as f:
            return jsonify(json.load(f)), 200
    return jsonify([]), 200

if __name__ == '__main__':
    os.makedirs(SHARED_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
