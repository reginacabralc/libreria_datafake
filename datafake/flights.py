import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing

fake = Faker()

def generate_flights(n=500, seed=42, missing_rate=0.0):
    # si al llamar la función no da parámetros, genera por default 500 filas con seed 42 y sin NaNs
    """
    Genera un conjunto de datos de vuelos.
    Parámetros:
    n : int
        Número de filas a generar
    semilla (seed): int
        Semilla aleatoria para garantizar la reproducibilidad
    tasa_faltante (missing_rate): float
        Proporción de valores faltantes a inyectar (0.0 a 1.0)
    Devuelve: pd.DataFrame
    """
    # inicializa la semilla aleatoria y en faker. Hay que fijar ambos para garantizar reproducibilidad
    np.random.seed(seed)
    Faker.seed(seed)
    
    # define listas con los valores posibles
    airlines = ["Delta", "United Airlines", "American", "Lufthansa", "Emirates",
                "Ryanair", "Air France", "British Airways", "Aeromexico", "LATAM"]
    airports = ["JFK", "LAX", "LHR", "CDG", "DXB", "NRT", "AICM", "GRU", "SYD", "FRA"]
    statuses = ["on_time", "delayed", "cancelled", "diverted"]
    classes = ["economy", "business", "first"]

    origins = np.random.choice(airports, size=n) # escoge aleatoriamente n aeropuertos de origen
    
    # Para cada origen o, filtra la lista de aeropuertos para excluir ese mismo aeropuerto (if a != o), 
    # y luego escoge uno al azar. Esto garantiza que ningún vuelo tenga origen igual a destino. 
    # El np.array() convierte la lista resultante en array de numpy.
    destinations = np.array([np.random.choice([a for a in airports if a != o]) for o in origins])
    
    # Genera n estatus de vuelo con probabilidades no uniformes: 70% a tiempo, 22% retrasado, 5% cancelado y 3% desviado. 
    # Estás probabilidades se escogen con la intensión de imitar la realidad del sector áereo en el mundo real
    flight_statuses = np.random.choice(statuses, size=n, p=[0.70, 0.22, 0.05, 0.03])

    df = pd.DataFrame({
        "flight_id": [f"FLT_{str(i).zfill(6)}" for i in range(1, n + 1)], #Genera IDs únicos tipo FLT_000001. zfill(6) rellena con ceros a la izquierda hasta tener 6 dígitos
        "date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(n)], # genera n fechas aleatorias entre hace 1 año y hoy
        "airline": np.random.choice(airlines, size=n), # escoge aleatoriamente n aerolíneas con probabilidad uniforme
        "origin": origins, # asigna el array que calculamos antes
        "destination": destinations, # asigna los array que calculamos antes
        "class": np.random.choice(classes, size=n, p=[0.75, 0.20, 0.05]), # Escoge clase de un vuelo con probabilidades no uniformes: 75% economy, 20% business y 5% primera clase (imitando la realidad)
        "duration_min": np.random.randint(60, 900, size=n), # Genera duración del vuelo en minutos con distribución uniforme entre 60 y 900 minutos. Este es el rango razonable para vyelos entre los aeropuertos de la lista
        "distance_km": np.random.randint(200, 15000, size=n), # Genera distancia en kilómetros con distribución uniforme entre 200 km y 15,000 km. Es uniforme porque sin saber el par origen-destino exacto no podemos calcular la distancia real. Sin embargo, estos rangos cubren las distancias entre los aeropuertos de nuestra lista 
        "price_usd": np.round(np.random.lognormal(mean=5.5, sigma=1.0, size=n), 2), # Genera precios con distribución lognormal (muchos vuelos baratos y pocos muy caros). Mean=5.5 en escala logarítmica equivale a un precio "típico" de 245 dólares
        "status": flight_statuses, # asigna el array que calculamos antes
        "delay_min": np.where(flight_statuses == "delayed", np.random.randint(15, 300, size=n), 0), # Si el estatus es "delayed" np.where asigna un número aleatorio entre 15 y 300 minutos, si no asigna 0
        "passengers": np.random.randint(50, 400, size=n), # Genera número de pasajeros con distribución uniforme entre 50 y 400 (aviones pequeños o grandes, vacíos o totalmente llenos)
        "satisfaction": np.round(np.random.uniform(1, 10, size=n), 1), # Genera una calificaci´øn de satisfacción entre 1,0 y 10.0 con distribución uniforme. Se usa uniforme porque en encuestas de satisfacción los valores extremos son muy comunes
    })

    # Antes de devolver el dataFrame, pasa por inject_missing. Si missing_rate=0.0 lo devuelve intacto, si no introduce NaNs en las columnas no protegidas
    return inject_missing(df, missing_rate=missing_rate, seed=seed)