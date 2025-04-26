from flask import Flask, render_template, jsonify
from utils.api_football import get_live_matches
from utils.football_data import get_team_profile
from utils.alert_logic import check_corner_alert
import os
import threading
import time
import requests

app = Flask(__name__)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Variável global para armazenar os jogos monitorados
live_matches_info = []

# Função de monitoramento em background
def monitor_matches():
    global live_matches_info
    while True:
        try:
            matches = get_live_matches()
            live_matches_info = []  # Limpa a lista antes de atualizar
            for match in matches:
                # Armazena informações importantes para o status
                live_matches_info.append({
                    "home_team": match['teams']['home']['name'],
                    "away_team": match['teams']['away']['name'],
                    "elapsed": match['fixture']['status']['elapsed'],
                    "status": match['fixture']['status']['short']
                })
                # Verifica se precisa enviar alerta
                alert = check_corner_alert(match)
                if alert:
                    send_telegram_alert(alert)
        except Exception as e:
            print("Erro no monitoramento:", e)
        time.sleep(60)  # Aguarda 1 min

# Envia mensagem no Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

@app.route("/")
def home():
    return render_template("index.html")

# Nova rota para ver o status dos jogos monitorados
@app.route("/status")
def status():
    return jsonify(live_matches_info)

if __name__ == "__main__":
    threading.Thread(target=monitor_matches).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
