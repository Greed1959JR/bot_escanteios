import requests
import os
import logging

logger = logging.getLogger(__name__)
API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')

def get_live_matches():
    try:
        url = 'https://api.sportmonks.com/v3/football/livescores'
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        params = {'include': 'localTeam,visitorTeam,stats'}
        
        logger.info("Buscando jogos ao vivo...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        matches = []
        
        for match in data['data']:
            match_info = {
                'id': match['id'],
                'home_team': match['localTeam']['data']['name'],
                'away_team': match['visitorTeam']['data']['name'],
                'minute': match['time']['minute'] if match['time'] else 0,
                'status': 'Ao Vivo',
                'teams': {
                    'home': {'id': match['localTeam']['data']['id'], 'name': match['localTeam']['data']['name']},
                    'away': {'id': match['visitorTeam']['data']['id'], 'name': match['visitorTeam']['data']['name']}
                },
                'statistics': match.get('stats', {}).get('data', [])
            }
            matches.append(match_info)
            
        logger.info(f"Retornando {len(matches)} partidas")
        return matches
        
    except Exception as e:
        logger.error(f"Erro ao buscar jogos: {str(e)}", exc_info=True)
        return []
