import pandas as pd
import numpy as np
from faker import Faker
from .utils import export_data, inject_missing, inject_noise

SUPPORTED_TYPES = [
    "int", "float", "normal", "lognormal", "bool",
    "category", "name", "email", "city", "country",
    "date", "text"
]

def generate_custom(schema: dict, n: int = 500, seed: int = 42, locale: str = "en_US", save_to: str = None, missing_rate: float = 0.0, noise_level: float = 0.0):
    """
    Genera un dataset sintético personalizado basado en un esquema definido por el usuario.

    Parámetros
    ----------
    schema : dict
        Diccionario donde cada key es el nombre de una columna y cada value
        es un diccionario con el tipo y parámetros de la columna.
    n : int
        Número de filas a generar.
    seed : int
        Semilla para reproducibilidad.
    locale : str
        Idioma para los datos generados por Faker.
    save_to : str
        Ruta del archivo destino (.csv o .xlsx). Opcional.
    missing_rate : float
        Proporción de valores faltantes (0.0 a 1.0).
    
    Tipos soportados
    ----------------
    - int        : {"type": "int", "min": 0, "max": 100}
    - float      : {"type": "float", "min": 0.0, "max": 1.0}
    - normal     : {"type": "normal", "mean": 0, "sigma": 1}
    - lognormal  : {"type": "lognormal", "mean": 5, "sigma": 1}
    - bool       : {"type": "bool", "p": 0.5}
    - category   : {"type": "category", "values": ["A","B","C"], "weights": [0.5,0.3,0.2]}
    - name       : {"type": "name"}
    - email      : {"type": "email"}
    - city       : {"type": "city"}
    - country    : {"type": "country"}
    - date       : {"type": "date", "start": "-2y", "end": "today"}
    - text       : {"type": "text"}

    Retorna
    -------
    pd.DataFrame
    """
    np.random.seed(seed)
    fake = Faker(locale)
    Faker.seed(seed)

    data = {}

    for col, config in schema.items():
        col_type = config.get("type")

        if col_type not in SUPPORTED_TYPES:
            raise ValueError(f"Tipo '{col_type}' no soportado. Tipos válidos: {SUPPORTED_TYPES}")

        if col_type == "int":
            min_val = config.get("min", 0)
            max_val = config.get("max", 100)
            data[col] = np.random.randint(min_val, max_val + 1, size=n)

        elif col_type == "float":
            min_val = config.get("min", 0.0)
            max_val = config.get("max", 1.0)
            data[col] = np.round(np.random.uniform(min_val, max_val, size=n), 2)

        elif col_type == "normal":
            mean = config.get("mean", 0)
            sigma = config.get("sigma", 1)
            data[col] = np.round(np.random.normal(mean, sigma, size=n), 2)

        elif col_type == "lognormal":
            mean = config.get("mean", 5)
            sigma = config.get("sigma", 1)
            data[col] = np.round(np.random.lognormal(mean, sigma, size=n), 2)

        elif col_type == "bool":
            p = config.get("p", 0.5)
            data[col] = np.random.choice([True, False], size=n, p=[p, 1 - p])

        elif col_type == "category":
            values = config.get("values", ["A", "B", "C"])
            weights = config.get("weights", None)
            if weights:
                weights = np.array(weights)
                weights = weights / weights.sum()
            data[col] = np.random.choice(values, size=n, p=weights)

        elif col_type == "name":
            data[col] = [fake.name() for _ in range(n)]

        elif col_type == "email":
            data[col] = [fake.email() for _ in range(n)]

        elif col_type == "city":
            data[col] = [fake.city() for _ in range(n)]

        elif col_type == "country":
            data[col] = [fake.country() for _ in range(n)]

        elif col_type == "date":
            start = config.get("start", "-1y")
            end = config.get("end", "today")
            data[col] = [fake.date_between(start_date=start, end_date=end) for _ in range(n)]

        elif col_type == "text":
            data[col] = [fake.sentence() for _ in range(n)]

    df = pd.DataFrame(data)

    if save_to:
        export_data(df, save_to)

    df = inject_noise(df, noise_level=noise_level, seed=seed)
    return inject_missing(df, missing_rate=missing_rate, seed=seed)