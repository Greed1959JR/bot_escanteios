import os
import requests

API_KEY = os.environ.get("API_FOOTBALL_KEY")
HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"

def get_live_matches():
    url = f"{BASE_URL}/fixtures?live=all"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data.get("response", [])
    return []
