import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data, inject_noise

# define la función con 4 parámetros (con parámetros default)
def generate_social(n=500, seed=42, missing_rate=0.0, save_to=None, locale="en_US", noise_level=0.0):
    """
    Genera un conjunto de datos sintético de publicaciones en redes sociales.
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
    platforms = ["Instagram", "Twitter", "TikTok", "Facebook", "LinkedIn"]
    content_types = ["image", "video", "text", "story", "reel"]
    topics = ["Food", "Travel", "Tech", "Fashion", "Sports", "Music", "Politics", "Health"]

    df = pd.DataFrame({
        "post_id": [f"POST_{str(i).zfill(6)}" for i in range(1, n + 1)], # genera IDs únicos tipo POST_000001
        "user_id": [f"USR_{str(np.random.randint(1, 201)).zfill(5)}" for _ in range(n)], # genera IDs de usuario entre 1 y 200 aleatoriamente (mismos usuarios aparecen muchas veces, un usuario con muchos posts)
        "platform": np.random.choice(platforms, size=n, p=[0.30, 0.25, 0.20, 0.15, 0.10]), # escoge plataforma con probabilidades no uniformes (basado en que app tiene más usuarios activos en la realidad)
        "content_type": np.random.choice(content_types, size=n, p=[0.30, 0.25, 0.20, 0.15, 0.10]), # escoge tipo de contenido con probabilidades no uniformes (imagen domina y reel es menos común (aunque está creciendo rápidamente))
        "topic": np.random.choice(topics, size=n), # escoge tema con probabilidad uniforme
        "date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(n)], # genera fechas en el último año usando Faker
        "likes": np.random.lognormal(mean=5, sigma=2, size=n).astype(int), # genera con distribución lognormal con media 5
        "comments": np.random.lognormal(mean=3, sigma=1.5, size=n).astype(int), # genera con distribución lognormal con media 3 (pues normalmente hay más likes que comentarios)
        "shares": np.random.lognormal(mean=2, sigma=1.5, size=n).astype(int), # genera con distribución lognormal con media 2 (pues normalmente hay más comentarios que shares)
        "reach": np.random.lognormal(mean=7, sigma=2, size=n).astype(int), # genera alcance con distribución lognormal con media 7 (siempre mayor que likes porque el alcance incluye personas que vieron el post pero no interactuaron)
        "followers_at_post": np.random.lognormal(mean=8, sigma=2, size=n).astype(int), # genera seguidores al momento del post con distribución lognormal con media 8 (muchas cuentas pequeñas y pocos influencers)
        "is_viral": np.random.choice([True, False], size=n, p=[0.05, 0.95]), # genera con distribución Bernoulli (solo el 5% de posts se vuelven virales, imitando la realidad donde la viralidad es un evento raro) 
    })
    
    # calcula el engagement rate usando la fórmula de marketing digital: suma de interacciones dividida entre alcance multiplicado por 100
    df["engagement_rate"] = np.round(
        (df["likes"] + df["comments"] + df["shares"]) / df["reach"] * 100, 2
    )

    if save_to: # guarda a csv o excel si se especifica
        export_data(df, save_to)

    df = inject_noise(df, noise_level=noise_level, seed=seed) # inyecta ruido antes de los missing para que los NaNs también puedan aparecer en valores ruidosos
    
    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)