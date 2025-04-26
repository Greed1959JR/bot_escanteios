import requests
import os
import logging

logger = logging.getLogger(__name__)
API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')

def get_live_matches():
    try:
        if not API_TOKEN:
            logger.error("Token da SportMonks não configurado")
            return []

        url = 'https://api.sportmonks.com/v3/football/livescores'
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        
        # Versão simplificada e testada da requisição
        params = {
            'include': 'participants',  # Removido stats temporariamente
            # Removido filters para teste inicial
        }
        
        logger.info(f"Requisitando jogos com parâmetros: {params}")
        
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        
        # Debug: Mostra a URL completa gerada
        logger.debug(f"URL completa da requisição: {response.url}")
        
        if response.status_code == 400:
            logger.error(f"Erro 400 - Resposta da API: {response.text}")
            return []
            
        response.raise_for_status()
        
        data = response.json()
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
                    }
                })
                
            except Exception as e:
                logger.error(f"Erro ao processar partida: {str(e)}")
                continue
                
        logger.info(f"Partidas processadas: {len(matches)}")
        return matches
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        return []
