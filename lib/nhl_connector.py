import requests


def get_latest_goal_of_teams(teams_scores: dict[str, int]):
    url = "https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.game.content.media.epg&site=en_nhlCA"
    response = requests.get(url)
    data = response.json()

    games = data["dates"][0]["games"]
    date = data["dates"][0]["date"]

    for game in games:
        status = game["status"]["abstractGameState"]
        home_team = game["teams"]["home"]["team"]["name"]
        away_team = game["teams"]["away"]["team"]["name"]

        if (
            status != "Live" or (
            home_team not in teams_scores
            and away_team not in teams_scores)
        ):
            continue

        home_away = "home" if home_team in teams_scores else "away"

        score = game["teams"][home_away]["score"]
        team = game["teams"][home_away]["team"]["name"]

        if score > teams_scores[team]:
                teams_scores[team] = score
                print(f"{team} scored goal #{score}!")
                return date, team

    return date, None
