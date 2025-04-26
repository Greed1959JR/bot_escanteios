import requests
import os
import logging

logger = logging.getLogger(__name__)
API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')

def get_live_matches():
    try:
        url = 'https://api.sportmonks.com/v3/football/livescores'
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        params = {
            'include': 'participants;stats',
            'filters': 'stateCodes:3'  # Somente jogos em andamento
        }
        
        logger.info("Buscando jogos ao vivo...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        matches = []
        
        for match in data.get('data', []):
            # Extrai os times corretamente da nova estrutura
            participants = match.get('participants', [])
            home_team = next((p for p in participants if p['meta']['location'] == 'home'), None)
            away_team = next((p for p in participants if p['meta']['location'] == 'away'), None)
            
            if not home_team or not away_team:
                continue
                
            match_info = {
                'id': match['id'],
                'home_team': home_team['name'],
                'away_team': away_team['name'],
                'minute': match.get('time', {}).get('minute', 0),
                'status': 'Ao Vivo',
                'teams': {
                    'home': {'id': home_team['id'], 'name': home_team['name']},
                    'away': {'id': away_team['id'], 'name': away_team['name']}
                },
                'statistics': match.get('stats', [])
            }
            matches.append(match_info)
            
        logger.info(f"Retornando {len(matches)} partidas")
        return matches
        
    except Exception as e:
        logger.error(f"Erro ao buscar jogos: {str(e)}", exc_info=True)
        return []
