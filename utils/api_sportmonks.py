import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_live_matches():
    """Busca partidas ao vivo automaticamente"""
    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        matches = []
        for event in response.json()['events']:
            matches.append({
                'id': event['id'],
                'home_team': event['homeTeam']['name'],
                'away_team': event['awayTeam']['name'],
                'minute': event['time']['scoreboardTime'],
                'status': 'AO VIVO'
            })
        return matches
    except Exception as e:
        logger.error(f"Erro ao buscar partidas: {e}")
        return []

def get_match_stats(match_id):
    """Pega estatísticas incluindo escanteios"""
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        stats = response.json()['statistics']
        corners = next((s for s in stats if s['group'] == 'Corners'), {'home': 0, 'away': 0})
        return {
            'corners_home': corners['home'],
            'corners_away': corners['away']
        }
    except:
        return {'corners_home': 0, 'corners_away': 0}
