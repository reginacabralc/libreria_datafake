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