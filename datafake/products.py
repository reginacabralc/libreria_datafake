import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data

def generate_products(n=50, seed=42, missing_rate=0.0, save_to=None, locale="en_US"):
    """
    Genera un dataset sintético de productos.
    Parámetros:
    n : int
        Número de productos a generar.
    seed : int
        Semilla para reproducibilidad.
    missing_rate : float
        Proporción de valores faltantes (0.0 a 1.0).
    save_to : str
        Ruta del archivo destino (.csv o .xlsx). Opcional.
    locale : str
        Idioma para los datos generados por Faker.
    Devuelve: pd.DataFrame
    """
    np.random.seed(seed)
    fake = Faker(locale)
    Faker.seed(seed)

    categories = ["Electronics", "Clothing", "Food", "Home", "Sports", "Beauty"]
    brands = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE"]

    df = pd.DataFrame({
        "product_id": [f"PROD_{str(i).zfill(4)}" for i in range(1, n + 1)],
        "name": [fake.catch_phrase() for _ in range(n)],
        "category": np.random.choice(categories, size=n, p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05]),
        "brand": np.random.choice(brands, size=n),
        "price": np.round(np.random.lognormal(mean=4.5, sigma=1.0, size=n), 2),
        "stock": np.random.randint(0, 500, size=n),
        "rating": np.round(np.random.uniform(1, 5, size=n), 1),
    })

    if save_to:
        export_data(df, save_to)

    return inject_missing(df, missing_rate=missing_rate, seed=seed)