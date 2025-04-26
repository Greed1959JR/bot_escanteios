import os
import requests

API_KEY = os.environ.get("FOOTBALL_DATA_KEY")
HEADERS = {
    "X-Auth-Token": API_KEY
}
BASE_URL = "https://api.football-data.org/v4"

def get_team_profile(team_id):
    url = f"{BASE_URL}/teams/{team_id}/matches?limit=5"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        matches = response.json().get("matches", [])
        corners = [m["cornerKicks"] for m in matches if "cornerKicks" in m]
        return sum(corners) / len(corners) if corners else 0
    return 0
