import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_live_matches():
    """Versão robusta para buscar partidas ao vivo"""
    try:
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Debug: Log completo da resposta (remova depois)
        logger.debug(f"Resposta completa: {data}")
        
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
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)
        return []

def get_match_stats(match_id):
    """Versão à prova de erros para estatísticas"""
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }, timeout=5)
        
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
