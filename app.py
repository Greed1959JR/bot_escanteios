from flask import Flask, render_template
from utils.api_sportmonks import get_live_matches
from utils.football_data import get_team_profile
from utils.alert_logic import check_corner_alert
import os
import threading
import time
import requests
import logging

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Lista para armazenar os jogos ao vivo
live_matches_status = []

# Função de monitoramento em background
def monitor_matches():
    global live_matches_status
    while True:
        try:
            matches = get_live_matches()
            if not matches:
                logger.warning("Nenhuma partida recebida - verifique conexão com a API")
                time.sleep(30)
                continue
                
            live_matches_status = matches  # Agora armazenamos a estrutura completa
            
            for match in matches:
                alert = check_corner_alert(match)
                if alert:
                    logger.info(f"Alerta: {alert}")
                    send_telegram_alert(alert)
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        
        time.sleep(60)

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Erro ao enviar para Telegram: {str(e)}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/status")
def status():
    logger.info(f"Acessando status - {len(live_matches_status)} partidas")
    return render_template("status.html", matches=live_matches_status)

# Inicia a thread antes de rodar o app
thread = threading.Thread(target=monitor_matches)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
