import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data, inject_noise

# define la función con 7 parámetros (con parámetros default)
def generate_sales(n=500, seed=42, start_date="2024-01-01", end_date="2024-12-31", missing_rate=0.0, save_to=None, locale="en_US", noise_level=0.0):
    """
    Genera un conjunto de datos de ventas sintético.

    Parámetros:
    n : int
        Número de filas a generar.
    seed : int
        Semilla aleatoria para reproducibilidad.
    start_date : str
        Fecha de inicio para las transacciones (AAAA-MM-DD).
    end_date : str
        Fecha de fin para las transacciones (AAAA-MM-DD).
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
    categories = ["Electronics", "Clothing", "Food", "Home", "Sports", "Beauty"]
    payment_methods = ["card", "transfer", "cash", "paypal"]
    statuses = ["completed", "returned", "pending"]
    # crea 200 IDs de clientes y 50 de productos
    # se crean antes del df para que los mismos IDs se repiran en múltiples filas, simulando que un cliente compra varias veces
    customer_ids = [f"CUST_{str(i).zfill(4)}" for i in range(1, 201)]
    product_ids = [f"PROD_{str(i).zfill(4)}" for i in range(1, 51)]
    # genera n fechas distribuidas uniformemente entre start_date y end_date
    dates = pd.date_range(start=start_date, end=end_date, periods=n)

    df = pd.DataFrame({
        "sale_id": [f"SALE_{str(i).zfill(6)}" for i in range(1, n + 1)], # genera IDs tipo SALE_000001 desde 1 hasta n+1, con zfill(6) rellena con ceros a la izquierda hasta tener 6 digitos
        "date": np.random.choice(dates, size=n), # escoge n fechas aleatoriamente del rango generado, se hace aleatorio para uqe las fechas no sean perfectamente secuenciales
        "customer_id": np.random.choice(customer_ids, size=n), # escoge IDs aleatoriamente del catálogo (con repetidos)
        "product_id": np.random.choice(product_ids, size=n), # escoge IDs aleatoriamente del catálogo (con repetidos)
        "category": np.random.choice(categories, size=n, p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05]), # escoge categoría con probabilidad no uniforme, imitando patrones reales de comercio (ecommerce)
        "quantity": np.random.randint(1, 10, size=n), # genera cantidades enteras entre 1 y 9 con distribución uniforme discreta
        "unit_price": np.round(np.random.lognormal(mean=4.5, sigma=1.0, size=n), 2), # genera precios con distribución lognormal (muchos productos baratos y pocos muy caros) 
        "payment_method": np.random.choice(payment_methods, size=n, p=[0.55, 0.25, 0.12, 0.08]), # escoge método con probabilidades no unfiromes (tarjeta domina y paypal es menos común)
        "status": np.random.choice(statuses, size=n, p=[0.88, 0.07, 0.05]), # escoge estatus con probabilidades no uniformes (la mayoría se completan y pocas quedan pendientes)
        "store": [fake.city() for _ in range(n)], # genera n nombres de ciudades usando Faker. El _ en el for loop indica que la variable iteradora no se usa, solo nos importa repetir la acción n veces
    })
    
    # 
    df["revenue"] = np.round(df["quantity"] * df["unit_price"], 2) # calcula el ingreso total como quantity*unit_price
    # convierte la columna date a formato fecha sin hora
    df["date"] = pd.to_datetime(df["date"]).dt.date

    if save_to:
        export_data(df, save_to) # guarda a csv o excel

    df = inject_noise(df, noise_level=noise_level, seed=seed) # inyecta ruido antes de los missing para que los NaNs también puedan aparecer en valores ruidosos
    
    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)