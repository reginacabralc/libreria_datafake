import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data, inject_noise

# define la función con 4 parámetros (con parámetros default)
def generate_movies(n=500, seed=42, missing_rate=0.0, save_to=None, locale="en_US", noise_level=0.0):
    """
    Genera un conjunto de datos sintético de películas/streaming.
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
    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Documentary", "Animation"]
    platforms = ["Netflix", "HBO Max", "Disney+", "Amazon Prime", "Apple TV+"]
    ratings = ["G", "PG", "PG-13", "R", "NC-17"]
    languages = ["English", "Spanish", "French", "Japanese", "Chinese", "Italian"]

    df = pd.DataFrame({
        "movie_id": [f"MOV_{str(i).zfill(5)}" for i in range(1, n + 1)], # genera ids únicos tipo MOV_00001
        "title": [fake.catch_phrase() for _ in range(n)], # genera frases cortas que se usan como títulos con Faker 
        "genre": np.random.choice(genres, size=n, p=[0.20, 0.15, 0.20, 0.10, 0.12, 0.10, 0.08, 0.05]), # escoge género con probabilidades no uniformes (acción y drama dominan y animación es el más raro porque hay menos películas animadas en streaming)
        "platform": np.random.choice(platforms, size=n, p=[0.35, 0.20, 0.20, 0.15, 0.10]), # escoge plataforma con probabilidades no uniformes (netflix domina porque tiene el catálogo más grande y Apple TV+ es el más pequeño por ser la plataforma más nueva)
        "release_year": np.random.randint(1970, 2025, size=n), # genera año de lanzamiento entre 1970 y 2024 con distribución uniforme discreta
        "duration_min": np.random.randint(75, 211, size=n), # genera duración entre 75 minutos (película corta) y 210 minutos (película muy larga) con distribución uniforme discreta
        "rating": np.random.choice(ratings, size=n, p=[0.05, 0.15, 0.40, 0.35, 0.05]), # escoge clasificación con probabilidades no uniformes (imitando la realidad)
        "language": np.random.choice(languages, size=n, p=[0.50, 0.20, 0.10, 0.08, 0.07, 0.05]), # escoge idioma con probabilidades no uniformes (inglés es el más usando en el mercado de cine)
        "imdb_score": np.round(np.random.normal(loc=6.5, scale=1.2, size=n).clip(1, 10), 1), # genera calificación con distribución normal centrada en 6.5 (usa normal porque pocas películas se clasifican en los extremos)
        "box_office_usd": np.random.lognormal(mean=17, sigma=2, size=n).astype(int), # genera ganancia en taquilla con lognormal con media 17 (la mayoría gana poca y algunas ganan mucho)
        "sequel": np.random.choice([True, False], size=n, p=[0.20, 0.80]), # genera con distribución Bernoulli (el 20% son secuelas, imitando proporciones reales de la industria)
    })

    if save_to: # guarda a csv o excel si se especifica
        export_data(df, save_to)

    df = inject_noise(df, noise_level=noise_level, seed=seed) # inyecta ruido antes de los missing para que los NaNs también puedan aparecer en valores ruidosos
    
    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)