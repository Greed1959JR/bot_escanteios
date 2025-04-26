from flask import Flask, render_template
from utils.footystats_api import get_live_matches
from utils.flashscore_scraper import get_live_corners
import os
import time
import threading

app = Flask(__name__)

# Configurações
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
UPDATE_INTERVAL = int(os.getenv('REQUEST_DELAY', 30))

live_data = []

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': message})

def monitor_matches():
    global live_data
    while True:
        try:
            # Tenta Footystats primeiro
            matches = get_live_matches()
            
            # Fallback para FlashScore
            if not matches:
                matches = get_live_corners()
            
            live_data = matches
            
            # Envia alertas
            for match in matches:
                if int(match.get('corners_home', 0)) >= 5:
                    msg = f"⚠️ {match['home']} está pressionando!\n"
                    msg += f"Escanteios: {match['corners_home']} (min. {match['minute']})"
                    send_telegram_alert(msg)
            
            time.sleep(UPDATE_INTERVAL)
            
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(60)

@app.route('/')
def home():
    return render_template('status.html', matches=live_data)

if __name__ == '__main__':
    threading.Thread(target=monitor_matches, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
