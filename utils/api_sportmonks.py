import os
import requests
import logging
import time
import random
from datetime import datetime

logger = logging.getLogger(__name__)

# Configurações
REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', '5'))  # Segundos entre requisições
LAST_REQUEST_TIME = 0

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

def get_match_stats(match_id):
    """Pega estatísticas incluindo escanteios de uma partida específica"""
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
        
        response = requests.get(
            url,
            headers=get_headers(),
            timeout=5
        )
        response.raise_for_status()
        
        stats = response.json().get('statistics', [])
        corners = next(
            (s for s in stats if s.get('group') == 'Corners'),
            {'home': 0, 'away': 0}
        )
        
        return {
            'corners_home': corners.get('home', 0),
            'corners_away': corners.get('away', 0),
            'last_update': datetime.now().strftime("%H:%M:%S")
        }
        
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {str(e)}")
        return {'corners_home': 0, 'corners_away': 0}

def get_live_matches():
    """Busca partidas ao vivo automaticamente"""
    global LAST_REQUEST_TIME
    
    # Respeita o delay entre requisições
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)
    
    try:
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"
        response = requests.get(
            url,
            headers=get_headers(),
            timeout=10
        )
        LAST_REQUEST_TIME = time.time()
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get('events'):
            logger.warning("Nenhuma partida ao vivo encontrada")
            return []
            
        return [{
            'id': event['id'],
            'home_team': event.get('homeTeam', {}).get('name', 'Desconhecido'),
            'away_team': event.get('awayTeam', {}).get('name', 'Desconhecido'),
            'minute': event.get('time', {}).get('scoreboardTime', 0),
            'status': 'AO VIVO'
        } for event in data['events']]
        
    except Exception as e:
        logger.error(f"Erro ao buscar partidas: {str(e)}")
        return []
