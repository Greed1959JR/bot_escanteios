import requests
import logging
import time
import random
from datetime import datetime

logger = logging.getLogger(__name__)

# Configurações
REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', '5'))  # Segundos entre requisições
LAST_REQUEST_TIME = 0

def make_request(url, headers=None):
    global LAST_REQUEST_TIME
    
    # Respeita o delay entre requisições
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)
    
    try:
        response = requests.get(
            url,
            headers=headers or {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'application/json'
            },
            timeout=10
        )
        LAST_REQUEST_TIME = time.time()
        return response
    except Exception as e:
        logger.error(f"Erro na requisição: {str(e)}")
        return None

def get_live_matches():
    # Tenta primeiro a API Football (se tiver chave)
    football_data_key = os.getenv('FOOTBALL_DATA_KEY')
    if football_data_key:
        try:
            response = make_request(
                "http://api.football-data.org/v4/matches",
                headers={'X-Auth-Token': football_data_key}
            )
            if response and response.status_code == 200:
                matches = []
                for match in response.json().get('matches', []):
                    if match['status'] == 'IN_PLAY':
                        matches.append({
                            'id': match['id'],
                            'home_team': match['homeTeam']['name'],
                            'away_team': match['awayTeam']['name'],
                            'minute': match.get('minute', 0),
                            'status': 'LIVE'
                        })
                if matches:
                    return matches
        except Exception as e:
            logger.error(f"Erro Football-Data: {str(e)}")

    # Fallback para SofaScore (com headers melhorados)
    try:
        response = make_request(
            "https://api.sofascore.com/api/v1/sport/football/events/live",
            headers={
                'User-Agent': random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                    "Mozilla/5.0 (X11; Linux x86_64)"
                ]),
                'Accept': '*/*',
                'Origin': 'https://www.sofascore.com',
                'Referer': 'https://www.sofascore.com/'
            }
        )
        
        if response and response.status_code == 200:
            data = response.json()
            return [{
                'id': event['id'],
                'home_team': event.get('homeTeam', {}).get('name', 'Unknown'),
                'away_team': event.get('awayTeam', {}).get('name', 'Unknown'),
                'minute': event.get('time', {}).get('scoreboardTime', 0),
                'status': 'LIVE'
            } for event in data.get('events', [])]
            
    except Exception as e:
        logger.error(f"Erro SofaScore: {str(e)}")
    
    return []
