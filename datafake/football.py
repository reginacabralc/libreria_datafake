import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_football(n=500, seed=42):
    """
    Generate a synthetic football matches dataset.

    Parameters
    ----------
    n : int
        Number of rows to generate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
    """
    np.random.seed(seed)
    Faker.seed(seed)

    teams = [
        "Real Madrid", "Barcelona", "Manchester City", "Liverpool",
        "Bayern Munich", "PSG", "Juventus", "Chelsea", "Arsenal",
        "Atletico Madrid", "Borussia Dortmund", "Inter Milan",
        "AC Milan", "Ajax", "Porto"
    ]
    competitions = ["La Liga", "Premier League", "Bundesliga", "Serie A", "Champions League"]
    stages = ["Group Stage", "Round of 16", "Quarter Final", "Semi Final", "Final", "Regular Season"]

    home_teams = np.random.choice(teams, size=n)
    away_teams = np.array([np.random.choice([t for t in teams if t != h]) for h in home_teams])

    home_goals = np.random.poisson(lam=1.5, size=n)
    away_goals = np.random.poisson(lam=1.1, size=n)

    def get_result(h, a):
        if h > a:
            return "home_win"
        elif a > h:
            return "away_win"
        else:
            return "draw"

    df = pd.DataFrame({
        "match_id": [f"MATCH_{str(i).zfill(5)}" for i in range(1, n + 1)],
        "date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(n)],
        "competition": np.random.choice(competitions, size=n, p=[0.25, 0.25, 0.20, 0.20, 0.10]),
        "stage": np.random.choice(stages, size=n),
        "home_team": home_teams,
        "away_team": away_teams,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "total_goals": home_goals + away_goals,
        "result": [get_result(h, a) for h, a in zip(home_goals, away_goals)],
        "attendance": np.random.randint(10000, 90000, size=n),
        "home_shots": np.random.randint(5, 25, size=n),
        "away_shots": np.random.randint(3, 20, size=n),
        "home_possession": np.round(np.random.uniform(35, 65, size=n), 1),
    })

    df["away_possession"] = np.round(100 - df["home_possession"], 1)

    return df.sort_values("date").reset_index(drop=True)