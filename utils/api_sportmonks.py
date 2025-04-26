import requests
import os

API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')

def get_live_matches():
    url = 'https://api.sportmonks.com/v3/football/livescores'
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    params = {
        'include': 'localTeam,visitorTeam'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        matches = []
        for match in data['data']:
            home_team = match['localTeam']['data']['name']
            away_team = match['visitorTeam']['data']['name']
            minute = match['time']['minute'] if match['time'] else 0

            matches.append({
                'home_team': home_team,
                'away_team': away_team,
                'minute': minute,
                'status': 'Ao Vivo'
            })
        return matches
    else:
        print(f"Erro ao buscar jogos: {response.status_code}")
        return []
