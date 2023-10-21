import os
from time import sleep

import pytz
from lib.nanoleaf_connector import turn_on_goal_effect, turn_on_weather_effect
from lib.nhl_connector import get_latest_goal_of_teams
import datetime
import pickle

from lib.weather_connector import get_weather_condition

TEAMS_SCORES_FILENAME = "team_scores.pkl"
DEFAULT_TEAMS =  {"Vancouver Canucks":0, "Calgary Flames": 0}

def main():
    teams = DEFAULT_TEAMS
    current_time = datetime.datetime.now(pytz.utc)

    pst_time = current_time.astimezone(pytz.timezone('US/Pacific'))
    cur_date = pst_time.date()
    last_weather_check = datetime.datetime(year=1999, month=1, day=1)

    print("Starting smart light server.")

    # Loads stored sate from file for game scores
    try:
        with open(TEAMS_SCORES_FILENAME, 'rb+') as fp:
            state = pickle.load(fp)
            if state["date"] == str(cur_date):
                teams = state["teams"]
                print(f'Team dictionary: {state}')
            else:
                print("Wrong date deleting file.")
    except FileNotFoundError:
        print("No score history.")


    while True:
        # checks for goal light
        try:
            date, scoring_team = get_latest_goal_of_teams(teams)
            if scoring_team is not None:
                turn_on_goal_effect(scoring_team.split()[1])
                with open(TEAMS_SCORES_FILENAME, 'wb+') as fp:
                    pickle.dump({"date":date, "teams":teams}, fp)
                print('dictionary saved successfully to file')

            if os.path.exists(TEAMS_SCORES_FILENAME) and str(cur_date) != date:
                os.remove(TEAMS_SCORES_FILENAME)
                teams = DEFAULT_TEAMS
                cur_date = date

            # Sets weather light
            if datetime.datetime.now() - last_weather_check > datetime.timedelta(minutes=5):
                last_weather_check = datetime.datetime.now()
                condition = get_weather_condition(os.environ['OPEN_WEATHER_API_KEY'], "New York")
                turn_on_weather_effect(condition)
        except Exception as e:
            print(f"Error {e} occurred.")
            
        sleep(5)



        


if __name__ == "__main__":
    main()