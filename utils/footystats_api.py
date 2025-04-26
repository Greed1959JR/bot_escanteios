import requests
import os

def get_live_matches():
    API_KEY = os.getenv('FOOTYSTATS_KEY')
    url = f"https://api.footystats.org/live?key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return [{
            'id': match['id'],
            'home': match['home_name'],
            'away': match['away_name'],
            'minute': match['time'],
            'corners_home': match['home_corners'],
            'corners_away': match['away_corners']
        } for match in data['data'] if match['home_corners'] is not None]
    except:
        return []
