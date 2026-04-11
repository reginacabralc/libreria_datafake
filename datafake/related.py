import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data, inject_noise

def generate_related(n_customers=200, n_products=50, n_sales=1000, seed=42, locale="en_US", missing_rate=0.0, noise_level=0.0, save_to=None):
    """
    Genera un conjunto de datasets relacionados con IDs consistentes
    para permitir joins entre tablas.

    Parámetros
    ----------
    n_customers : int
        Número de clientes a generar.
    n_products : int
        Número de productos a generar.
    n_sales : int
        Número de transacciones de venta a generar.
    seed : int
        Semilla para reproducibilidad.
    locale : str
        Idioma para los datos generados por Faker.
    missing_rate : float
        Proporción de valores faltantes (0.0 a 1.0).
    noise_level : float
        Nivel de ruido a agregar a columnas numéricas (0.0 a 1.0).
    save_to : str
        Carpeta destino para guardar los tres archivos CSV. Opcional.

    Retorna
    -------
    dict con keys: 'customers', 'products', 'sales'
    """
    np.random.seed(seed)
    fake = Faker(locale)
    Faker.seed(seed)

    # ── CLIENTES ──────────────────────────────
    segments = ["premium", "regular", "occasional"]
    customer_ids = [f"CUST_{str(i).zfill(4)}" for i in range(1, n_customers + 1)]

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "name": [fake.name() for _ in range(n_customers)],
        "email": [fake.email() for _ in range(n_customers)],
        "city": [fake.city() for _ in range(n_customers)],
        "country": [fake.country() for _ in range(n_customers)],
        "age": np.random.randint(18, 70, size=n_customers),
        "segment": np.random.choice(segments, size=n_customers, p=[0.20, 0.55, 0.25]),
        "registration_date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(n_customers)],
    })

    # ── PRODUCTOS ─────────────────────────────
    categories = ["Electronics", "Clothing", "Food", "Home", "Sports", "Beauty"]
    brands = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE"]
    product_ids = [f"PROD_{str(i).zfill(4)}" for i in range(1, n_products + 1)]

    products = pd.DataFrame({
        "product_id": product_ids,
        "name": [fake.catch_phrase() for _ in range(n_products)],
        "category": np.random.choice(categories, size=n_products, p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05]),
        "brand": np.random.choice(brands, size=n_products),
        "price": np.round(np.random.lognormal(mean=4.5, sigma=1.0, size=n_products), 2),
        "stock": np.random.randint(0, 500, size=n_products),
        "rating": np.round(np.random.uniform(1, 5, size=n_products), 1),
    })

    # ── VENTAS ────────────────────────────────
    payment_methods = ["card", "transfer", "cash", "paypal"]
    statuses = ["completed", "returned", "pending"]
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", periods=n_sales)

    sampled_customers = np.random.choice(customer_ids, size=n_sales)
    sampled_products = np.random.choice(product_ids, size=n_sales)

    product_price_map = dict(zip(products["product_id"], products["price"]))
    prices = np.array([product_price_map[pid] for pid in sampled_products])

    quantities = np.random.randint(1, 10, size=n_sales)

    sales = pd.DataFrame({
        "sale_id": [f"SALE_{str(i).zfill(6)}" for i in range(1, n_sales + 1)],
        "date": np.random.choice(dates, size=n_sales),
        "customer_id": sampled_customers,
        "product_id": sampled_products,
        "quantity": quantities,
        "unit_price": np.round(prices, 2),
        "payment_method": np.random.choice(payment_methods, size=n_sales, p=[0.55, 0.25, 0.12, 0.08]),
        "status": np.random.choice(statuses, size=n_sales, p=[0.88, 0.07, 0.05]),
        "revenue": np.round(quantities * prices, 2),
    })

    sales["date"] = pd.to_datetime(sales["date"]).dt.date

    # ── RUIDO ─────────────────────────────────
    customers = inject_noise(customers, noise_level=noise_level, seed=seed)
    products = inject_noise(products, noise_level=noise_level, seed=seed)
    sales = inject_noise(sales, noise_level=noise_level, seed=seed)

    # ── VALORES FALTANTES ─────────────────────
    customers = inject_missing(customers, missing_rate=missing_rate, seed=seed)
    products = inject_missing(products, missing_rate=missing_rate, seed=seed)
    sales = inject_missing(sales, missing_rate=missing_rate, seed=seed)

    # ── EXPORTAR ──────────────────────────────
    if save_to:
        import os
        os.makedirs(save_to, exist_ok=True)
        export_data(customers, f"{save_to}/customers.csv")
        export_data(products, f"{save_to}/products.csv")
        export_data(sales, f"{save_to}/sales.csv")

    return {
        "customers": customers,
        "products": products,
        "sales": sales,
    }