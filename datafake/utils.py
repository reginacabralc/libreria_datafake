import numpy as np
import pandas as pd

# definimos la función que recibe 3 parámetros. 
def inject_missing(df: pd.DataFrame, missing_rate: float = 0.0, seed: int = None):
    """
    Inyecta valores NaN aleatoriamente en un DataFrame.
    Parámetros:
    df : pd.DataFrame
        El DataFrame al que se le inyectarán valores NaNs.
    missing_rate : float
        Proporción de valores a convertir en NaN (0.0 a 1.0).
        Las columnas de ID y fechas están protegidas y nunca reciben NaNs.
        Por default es 0.
    seed : int
        Semilla aleatoria para reproducibilidad.
    Devuelve: pd.DataFrame
    """
    # si no se piden NaNs devuelve inmediatamente el DataFrame sin hacer cambios
    if missing_rate == 0.0:
        return df

    # verifica que el valor esté entre 0 y 1, si no lanza una excepción
    if not 0.0 < missing_rate < 1.0:
        raise ValueError("missing_rate must be between 0.0 and 1.0 (exclusive)")

    # fija la semilla si es que el usuario pasó una
    if seed is not None:
        np.random.seed(seed)

    # construye una lista de columnas protegidas que NUNCA deben tener NaNs
    # recorre todo el df y guarda solo las que terminen en id o que sean exactamente "date", "visit_date" o "registration_date"
    protected = [col for col in df.columns if any([
        col.endswith("_id"),
        col.endswith("id"),
        col == "date",
        col == "visit_date",
        col == "registration_date",
    ])]

    # hace una copia del df antes de modificarlo
    df = df.copy()

    # recorre cada columna. Si está en la lista de protegidas la salta y pasa a la siguiente
    for col in df.columns:
        if col in protected:
            continue
        # genera un array de True/False del mismo largo que el df
        # np.random.random() produce números entre 0 y 1, los que caen por debajo de missing_rate se vuelven True
        mask = np.random.random(size=len(df)) < missing_rate
        # donde mask es True, reemplaza el valor de esa celda por NaN
        df.loc[mask, col] = np.nan
    # devuelve el df
    return df

def export_data(df: pd.DataFrame, path: str):
    """
    Exporta un DataFrame a CSV o Excel según la extensión del archivo.
    Parámetros: 
    df : pd.DataFrame
        El DataFrame a exportar.
    path : str
        Ruta del archivo destino. Usa .csv para CSV o .xlsx para Excel.
    Devuelve: None
    """
    if path.endswith(".csv"):
        df.to_csv(path, index=False)
        print(f"Archivo guardado en: {path}")
    elif path.endswith(".xlsx"):
        df.to_excel(path, index=False)
        print(f"Archivo guardado en: {path}")
    else:
        raise ValueError("El archivo debe tener extensión .csv o .xlsx")
    
def describe_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un resumen detallado de un DataFrame sintético.
    Parámetros:
    df : pd.DataFrame
        El DataFrame a describir.
    Devuelve: pd.DataFrame
    """
    
    rows = []

    for col in df.columns:
        serie = df[col]
        info = {
            "columna": col,
            "tipo": str(serie.dtype),
            "nulos": serie.isnull().sum(),
            "pct_nulos": round(serie.isnull().mean() * 100, 1),
            "unicos": serie.nunique(),
        }

        if pd.api.types.is_numeric_dtype(serie):
            info["min"] = round(serie.min(), 2) if not serie.isnull().all() else None
            info["max"] = round(serie.max(), 2) if not serie.isnull().all() else None
            info["media"] = round(serie.mean(), 2) if not serie.isnull().all() else None
            info["desv_std"] = round(serie.std(), 2) if not serie.isnull().all() else None
            info["valores_frecuentes"] = None
        else:
            info["min"] = None
            info["max"] = None
            info["media"] = None
            info["desv_std"] = None
            top = serie.value_counts().head(3)
            info["valores_frecuentes"] = ", ".join([f"{v}({c})" for v, c in top.items()])

        rows.append(info)

    resultado = pd.DataFrame(rows)
    resultado = resultado.set_index("columna")
    return resultado

def inject_noise(df: pd.DataFrame, noise_level: float = 0.0, seed: int = None) -> pd.DataFrame:
    """
    Agrega ruido aleatorio y outliers controlados a columnas numéricas continuas.
    Parámetros:
    df : pd.DataFrame
        El DataFrame al que se le agregará ruido.
    noise_level : float
        Nivel de ruido a agregar (0.0 a 1.0).
        Por ejemplo, 0.1 agrega perturbaciones de hasta ±10% en columnas numéricas
        y genera outliers extremos en ~2% de los valores.
    seed : int
        Semilla para reproducibilidad.
    Devuelve: pd.DataFrame
    """
    if noise_level == 0.0:
        return df

    if not 0.0 < noise_level < 1.0:
        raise ValueError("noise_level debe estar entre 0.0 y 1.0 (exclusivo)")

    if seed is not None:
        np.random.seed(seed)

    # Columnas protegidas que nunca reciben ruido
    protected = [col for col in df.columns if any([
        col.endswith("_id"),
        col.endswith("id"),
        col == "date",
        col == "visit_date",
        col == "registration_date",
        col == "result",
        col == "status",
        col == "payment_method",
        col == "churned",
        col == "incumbent",
        col == "is_viral",
        col == "smoker",
        col == "chronic_condition",
        col == "sequel",
        col == "explicit",
    ])]

    df = df.copy()

    for col in df.columns:
        if col in protected:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue
        if df[col].isnull().all():
            continue

        # Ruido gaussiano — perturbación de ±noise_level
        std = df[col].std()
        if std == 0:
            continue

        noise = np.random.normal(0, noise_level * std, size=len(df))
        df[col] = df[col] + noise

        # Outliers extremos — ~2% de los valores se vuelven muy extremos
        outlier_mask = np.random.random(size=len(df)) < (noise_level * 0.2)
        outlier_values = df[col].mean() + np.random.choice([-1, 1], size=outlier_mask.sum()) * std * np.random.uniform(3, 6, size=outlier_mask.sum())
        df.loc[outlier_mask, col] = outlier_values

        # Redondear si la columna original era entera
        if pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].round().astype(int)
        else:
            df[col] = np.round(df[col], 2)

    return df