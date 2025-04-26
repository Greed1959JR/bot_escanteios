from bs4 import BeautifulSoup
import requests

def get_live_corners():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get("https://www.flashscore.com", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        corners = []
        for match in soup.select('div.event__match--live'):
            teams = [t.text for t in match.select('.event__participant')]
            corner = match.select_one('.event__soccerStat--corners')
            if corner:
                corners.append({
                    'home': teams[0],
                    'away': teams[1],
                    'corners': corner.text.split()[0]
                })
        return corners
    except:
        return []
