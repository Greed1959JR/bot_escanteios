import requests
import logging
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

# Lista de User-Agents válidos
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.sofascore.com/",
        "Origin": "https://www.sofascore.com"
    }

def get_live_matches():
    try:
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"
        
        # Adicionando timestamp para evitar cache
        params = {
            "_": str(int(time.time() * 1000))
        }
        
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=10
        )
        
        # Debug avançado
        logger.debug(f"Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        
        if response.status_code == 403:
            raise Exception("Acesso bloqueado - Atualize os headers ou use VPN")
            
        response.raise_for_status()
        data = response.json()
        
        if not data.get('events'):
            return []
            
        return [{
            'id': event['id'],
            'home_team': event.get('homeTeam', {}).get('name', 'Unknown'),
            'away_team': event.get('awayTeam', {}).get('name', 'Unknown'),
            'minute': event.get('time', {}).get('scoreboardTime', 0),
            'status': 'LIVE'
        } for event in data['events']]
        
    except Exception as e:
        logger.error(f"Erro ao buscar partidas: {str(e)}")
        return []
