from utils.football_data import get_team_profile

def check_corner_alert(match):
    stats = match.get("statistics", [])
    if not stats: return None

    home_team = match["teams"]["home"]["id"]
    away_team = match["teams"]["away"]["id"]

    home_avg = get_team_profile(home_team)
    away_avg = get_team_profile(away_team)

    for team_stats in stats:
        team_name = team_stats["team"]["name"]
        stats_list = team_stats["statistics"]
        possession = next((s["value"] for s in stats_list if s["type"] == "Ball Possession"), "0%")
        attacks = next((s["value"] for s in stats_list if s["type"] == "Dangerous Attacks"), 0)

        if int(possession.strip('%')) > 52 and int(attacks) >= 5:
            if team_name == match["teams"]["home"]["name"] and home_avg >= 6:
                return f"🔔 Tendência de escanteios: {team_name} pressionando com média de {home_avg:.1f}"
            elif team_name == match["teams"]["away"]["name"] and away_avg >= 6:
                return f"🔔 Tendência de escanteios: {team_name} pressionando com média de {away_avg:.1f}"
    return None
