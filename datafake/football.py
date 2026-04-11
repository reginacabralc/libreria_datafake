import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data

# define la función con 4 parámetros (con parámetros default)
def generate_football(n=500, seed=42, missing_rate=0.0, save_to=None, locale="en_US"):
    """
    Genera un conjunto de datos sintético de partidos de fútbol.
    Parámetros:
    n : int
        Número de filas a generar.
    seed : int
        Semilla aleatoria para reproducibilidad.
    missing_rate : float
        Proporción de valores faltantes a inyectar (0.0 a 1.0).
    Devuelve: pd.DataFrame
    """
    # crea una instancia de Faker con el locale
    fake = Faker(locale)
    
    # fija la semilla en numpy y en Faker por separado para garantizar reproducibilidad completa
    np.random.seed(seed)
    Faker.seed(seed)

    # define los valores posibles para las columnas categóricas
    teams = [
        "Real Madrid", "Barcelona", "Manchester City", "Liverpool",
        "Bayern Munich", "PSG", "Juventus", "Chelsea", "Arsenal",
        "Atletico Madrid", "Borussia Dortmund", "Inter Milan",
        "AC Milan", "Ajax", "Porto"
    ]
    competitions = ["La Liga", "Premier League", "Bundesliga", "Serie A", "Champions League"]
    stages = ["Group Stage", "Round of 16", "Quarter Final", "Semi Final", "Final", "Regular Season"]

    # escofe n equipos locales aleatoriamente de la lista con probabilidad uniforme
    home_teams = np.random.choice(teams, size=n)
    # para cada equipo local h, filtra la lista para excluirlo y escoge un visitante al azar (garantiza que ningún equipo juegue contra sí mismo)
    away_teams = np.array([np.random.choice([t for t in teams if t != h]) for h in home_teams])
    # genera goles con distribución Poisson (el equipo local tiene lam=1.5 y el visitante lam=1.1 porque estadísticamente los equipos locales marcan más goles (fenómeno conocido como "ventaja de local"))
    home_goals = np.random.poisson(lam=1.5, size=n)
    away_goals = np.random.poisson(lam=1.1, size=n)

    # función auxiliar que recibe los goles de ambos equipos y devuelve el resultado textual
    def get_result(h, a):
        if h > a:
            return "home_win"
        elif a > h:
            return "away_win"
        else:
            return "draw"

    df = pd.DataFrame({
        "match_id": [f"MATCH_{str(i).zfill(5)}" for i in range(1, n + 1)], # genera ids únicos tipo MATCH_00001
        "date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(n)], # genera n fechas aleatorias en los últimos 3 años usando faker
        "competition": np.random.choice(competitions, size=n, p=[0.25, 0.25, 0.20, 0.20, 0.10]), # escoge competición con probabilidades no uniformes (La Liga y Premier League son las más comunes y Champion League la menos porque tiene menos partidos que una liga completa)
        "stage": np.random.choice(stages, size=n), # escoge etapa con probabilidad uniforme
        "home_team": home_teams, # asigna el array generado antes 
        "away_team": away_teams, # asigna el array generado antes 
        "home_goals": home_goals, # asigna el array generado antes 
        "away_goals": away_goals, # asigna el array generado antes 
        "total_goals": home_goals + away_goals, # suma los goles de ambos equipos
        "result": [get_result(h, a) for h, a in zip(home_goals, away_goals)], # aplica la función auxiliar a cada par de goles
        "attendance": np.random.randint(10000, 90000, size=n), # genera asistencia con distribución uniforme discreta entre 10,000 y 90,000 (cubre desde estadios pequeños hasta los más grandes)
        "home_shots": np.random.randint(5, 25, size=n), # genera tiros con distribución uniforme discreta (rango 5-24)
        "away_shots": np.random.randint(3, 20, size=n), # genera tiros con distribución uniforme discreta (rango 3-19 por "ventaja de local")
        "home_possession": np.round(np.random.uniform(35, 65, size=n), 1), # genera con posesión local con distribución uniforme continua entre 35% y 65% (se limira a ese intervalo porque en fútbol profesional es muy raro ver algo fuera de ese intervalo)
    })

    # calcula la posesión visitante como complemento de la local (ambas deben sumar 100%)
    df["away_possession"] = np.round(100 - df["home_possession"], 1)

    if save_to: # guarda a csv o excel si se especifica
        export_data(df, save_to)
    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)