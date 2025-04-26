import requests
import os
import logging

logger = logging.getLogger(__name__)
API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')
BASE_URL = "https://api.sportmonks.com/v3"

def get_live_matches():
    try:
        if not API_TOKEN:
            logger.error("Token da SportMonks não configurado")
            return []

        endpoint = "/football/livescores"
        url = f"{BASE_URL}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Versão ultra-simplificada para teste
        params = {
            "per_page": 5  # Limita a 5 resultados para teste
        }
        
        logger.info(f"Requisitando: {url} com headers: {headers.keys()}")
        
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )
        
        # Debug avançado
        logger.debug(f"Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Content: {response.text[:200]}...")  # Mostra apenas início do conteúdo
        
        if response.status_code != 200:
            logger.error(f"Erro {response.status_code} - Resposta: {response.text}")
            return []
            
        data = response.json()
        
        if not isinstance(data, dict) or 'data' not in data:
            logger.error("Resposta inesperada da API")
            return []
            
        matches = []
        
        for match in data['data']:
            try:
                match_info = {
                    'id': match['id'],
                    'status': match.get('status_description', 'Desconhecido'),
                    'time': match.get('time', {}).get('minute', 0)
                }
                matches.append(match_info)
            except Exception as e:
                logger.error(f"Erro ao processar partida: {str(e)}")
                continue
                
        logger.info(f"Partidas recebidas (formato básico): {matches}")
        return matches
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        return []
