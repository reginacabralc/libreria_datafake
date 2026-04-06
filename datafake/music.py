import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing

# crea una instancia global de Faker 
fake = Faker()

# define la función con 3 parámetros (con parámetros default)
def generate_music(n=500, seed=42, missing_rate=0.0):
    """
    Genera un conjunto de datos sintético de streaming de música.
    Parámetros:
    n : int
        Número de filas a generar.
    seed : int
        Semilla aleatoria para reproducibilidad.
    missing_rate : float
        Proporción de valores faltantes a inyectar (0.0 a 1.0).
    Devuelve: pd.DataFrame
    """
    # fija la semilla en numpy y en Faker por separado para garantizar reproducibilidad completa
    np.random.seed(seed)
    Faker.seed(seed)

    # define los valores posibles para las columnas categóricas
    genres = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz", "Classical", "Reggaeton", "R&B"]
    moods = ["Happy", "Sad", "Energetic", "Chill", "Romantic", "Angry"]
    platforms = ["Spotify", "Apple Music", "YouTube Music", "Tencent Music", "Amazon Music"]

    df = pd.DataFrame({
        "track_id": [f"TRK_{str(i).zfill(6)}" for i in range(1, n + 1)], # genera ids únicos tipo TRK_000001 (no hay eventos repetidas en el dataset)
        "title": [fake.catch_phrase() for _ in range(n)], # usa catch_phrase() de Faker para generar títulos (genera frases de 2-4 palabras que funcionan como títulos creativos)
        "artist": [fake.name() for _ in range(n)], # usa fake.name() para generar nombres de artistas
        "album": [fake.bs() for _ in range(n)], # usa bs() de Faker (genera frases abstractas que funcionan como nombres de albúmes)
        "genre": np.random.choice(genres, size=n, p=[0.25, 0.15, 0.20, 0.10, 0.05, 0.05, 0.12, 0.08]), # escoge género con probabilidades no uniformes (basado en la cantidad de oyentes en plataformas de streaming)
        "mood": np.random.choice(moods, size=n), # escoge estado de ánimo con probabilidad uniforme
        "duration_seconds": np.random.randint(120, 360, size=n), # genera duración en segundos entre 120 y 359 (casi 6 min) con distribución uniforme
        "release_year": np.random.randint(1980, 2025, size=n), # gener año de lanzamiento entre 1980 y 2024 con distribución uniforme
        "streams": np.random.lognormal(mean=12, sigma=2, size=n).astype(int), # genera reproducciones con distribución lognormal (la mayoría de las canciones tienen pocas reproducciones y unas pocas tienen muchas)
        "likes": np.random.lognormal(mean=8, sigma=2, size=n).astype(int), # genera likes con distribución lognormal
        "platform": np.random.choice(platforms, size=n, p=[0.40, 0.25, 0.20, 0.08, 0.07]), # escoge plataforma con probabilidad no uniforme 
        "explicit": np.random.choice([True, False], size=n, p=[0.30, 0.70]), # se genera con distribución Bernoulli 
        "bpm": np.random.randint(60, 180, size=n), # genera bpm entre 60 y 179 con distribución uniforme discreta
        "rating": np.round(np.random.uniform(1, 5, size=n), 1), # genera calificación entre 1.0 y 5.o con distribución uniforme continua
    })

    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)