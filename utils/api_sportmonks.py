import requests
import os
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)
API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')

def get_live_matches():
    try:
        if not API_TOKEN:
            logger.error("Token da SportMonks não configurado")
            return []

        url = 'https://api.sportmonks.com/v3/football/livescores'
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        
        # Parâmetros corrigidos e codificados manualmente
        params = {
            'include': 'participants;stats',
            'filters': 'stateCodes:3'  # Jogos em andamento
        }
        
        logger.info(f"Requisitando jogos com parâmetros: {params}")
        
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        
        # Verificação adicional do status code
        if response.status_code == 409:
            logger.error("Erro 409 - Verifique os parâmetros da requisição")
            return []
            
        response.raise_for_status()
        
        data = response.json()
        
        # Debug: Log da resposta completa (remova depois de testar)
        logger.debug(f"Resposta completa da API: {data}")
        
        matches = []
        
        for match in data.get('data', []):
            try:
                participants = match.get('participants', [])
                home_team = next((p for p in participants if p['meta']['location'] == 'home'), None)
                away_team = next((p for p in participants if p['meta']['location'] == 'away'), None)
                
                if not home_team or not away_team:
                    continue
                    
                matches.append({
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
                })
                
            except Exception as e:
                logger.error(f"Erro ao processar partida {match.get('id')}: {str(e)}")
                continue
                
        logger.info(f"Partidas processadas: {len(matches)}")
        return matches
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        return []
