import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data, inject_noise

# define la función con 8 parámetros (con parámetros default)
# tiene sentido controlar el rango de fechas porque es clima
def generate_weather(n=500, seed=42, start_date="2024-01-01", end_date="2024-12-31", missing_rate=0.0, save_to=None, locale="en_US", noise_level=0.0):
    """
    Genera un conjunto de datos de clima sintético.
    Parámetros:
    n : int
        Número de filas a generar.
    seed : int
        Semilla aleatoria para reproducibilidad.
    start_date : str
        Fecha de inicio (AAAA-MM-DD).
    end_date : str
        Fecha de fin (AAAA-MM-DD).
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
    cities = [
        "Mexico City", "New York", "London", "Tokyo", "Paris",
        "Sydney", "Toronto", "Berlin", "Dubai", "São Paulo"
    ]
    conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Windy", "Foggy"] # cubren lo que cualquier ciudad de la lista podría experimentar

    # genera n fechas distribuidas uniformemente entre start_date y end_date
    dates = pd.date_range(start=start_date, end=end_date, periods=n)

    df = pd.DataFrame({
        "record_id": [f"WTH_{str(i).zfill(6)}" for i in range(1, n + 1)], # genera IDs únicos tipo WTH_000001
        "date": np.random.choice(dates, size=n), # escoge n fechas aleatoriamente del rango generado para que no sean perfectamente secuenciales
        "city": np.random.choice(cities, size=n), # escoge ciudad con probabilidad uniforme
        "temperature_c": np.round(np.random.normal(loc=18, scale=12, size=n), 1), # genera temperatura con distribución normal, con media 18C y variación 12C amplia que cubre ciduades frías (como Toronto) hasta calurosas (como Dubai)
        "humidity_pct": np.round(np.random.uniform(20, 100, size=n), 1), # genera humedad con distribución uniforme continua entre 20% y 100%
        "wind_speed_kmh": np.round(np.random.lognormal(mean=2.5, sigma=0.8, size=n), 1), # genera velocidad del viento con distribución lognormal (mucho viento suave, a veces viento fuerte)
        "precipitation_mm": np.round(np.random.exponential(scale=5, size=n), 1), # genera precipitación con distribución exponencial (la mayoría de días llueve poco o nada, y ocasionalmente llueve mucho. Sigue comportamiento real de la lluvia)
        "condition": np.random.choice(conditions, size=n, p=[0.30, 0.25, 0.20, 0.08, 0.07, 0.06, 0.04]), # escoge condición con probabilidades no uniformes
        "uv_index": np.random.randint(0, 11, size=n), # genera índice UV entre 0 y 10 con distribución uniforme discreta (no incluimos 11 en el índice porque es un extremo poco común globalmente)
        "visibility_km": np.round(np.random.uniform(1, 30, size=n), 1), # genera visibilidad entre 1km (día nublado) y 30km (día despejado) con distribución uniforme continua
    })

    # convierte la columna date a fecha sin componente de hora
    df["date"] = pd.to_datetime(df["date"]).dt.date

    if save_to: # guarda a csv o excel si se especifica
        export_data(df, save_to)

    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)