import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing

# crea una instancia global de Faker 
fake = Faker()

# define la función con 3 parámetros (con parámetros default)
# el default de n es 300 en lugar de 500 porque una base de clientes típicamente tiene menos registros que número de transacciones
def generate_users(n=300, seed=42, missing_rate=0.0):
    """
    Genera un conjunto de datos de usuarios sintético.

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
    plans = ["free", "basic", "pro", "enterprise"]
    devices = ["mobile", "desktop", "tablet"]
    statuses = ["active", "inactive", "churned"]

    df = pd.DataFrame({
        "user_id": [f"USR_{str(i).zfill(5)}" for i in range(1, n + 1)], # genera ids únicos tipo USR_00001
        "name": [fake.name() for _ in range(n)], # usa faker para generar nombres realistas
        "email": [fake.email() for _ in range(n)], # usa faker para generar emails realistas
        "country": [fake.country() for _ in range(n)], # usa faker para generar países realistas
        "age": np.random.randint(18, 71, size=n), # genera edades entre 18 y 70 con distribución uniforme discreta (asume usuarios adultos)
        "plan": np.random.choice(plans, size=n, p=[0.55, 0.25, 0.15, 0.05]), # escoge plan con probabilidades no uniformes (la mayoría plan gratuito, muy pocos enterprise)
        "device": np.random.choice(devices, size=n, p=[0.55, 0.35, 0.10]), # escoge dispositivo con probabilidades no unfiromes (la mayoría mobile y pocos tablet)
        "sessions_per_month": np.random.poisson(lam=12, size=n), # genera número de sesiones mensaules con distribución poisson. Poisson porque modela conteos de eventos en el tiempo (promedio de 12 al mes)
        "avg_session_minutes": np.round(np.random.lognormal(mean=2.5, sigma=0.8, size=n), 1), # genera duración promedio de sesión con distribución lognormal (la mayoría cortas pero algunas largas)
        "status": np.random.choice(statuses, size=n, p=[0.70, 0.20, 0.10]), # escoge estatus con probabilidades no uniformes
        "registration_date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(n)], # genera fechas de registro en los últimos 3 años usando Faker
    })

    # crea una columna binaria que se deriva del status, donde status es "churned" pone 1, en los demás 0. Convierte la columna de True/False a entero 1/0
    df["churned"] = (df["status"] == "churned").astype(int)
    
    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)