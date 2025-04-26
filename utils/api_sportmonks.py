import os
import requests
import logging
import time
from bs4 import BeautifulSoup
from datetime import datetime

logger = logging.getLogger(__name__)

def get_live_matches():
    """Busca partidas ao vivo via Flashscore"""
    try:
        url = "https://www.flashscore.com"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "pt-BR,pt;q=0.9"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []
        
        for match in soup.select('div[class^="event__match"]'):
            try:
                match_id = match['id'].split('_')[-1]
                home_team = match.select_one('.event__participant--home').text.strip()
                away_team = match.select_one('.event__participant--away').text.strip()
                minute = match.select_one('.event__stage--block').text.strip()
                
                matches.append({
                    'id': match_id,
                    'home_team': home_team,
                    'away_team': away_team,
                    'minute': minute,
                    'status': 'AO VIVO'
                })
            except Exception as e:
                logger.debug(f"Ignorando partida: {str(e)}")
                continue
                
        return matches[:20]  # Limita a 20 partidas
        
    except Exception as e:
        logger.error(f"Erro Flashscore: {str(e)}")
        return []

def get_match_stats(match_id):
    """Retorna dados simulados (Flashscore não fornece API direta)"""
    return {
        'corners_home': random.randint(0, 10),
        'corners_away': random.randint(0, 8),
        'last_update': datetime.now().strftime("%H:%M:%S")
    }
