import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data 

# define la función con 4 parámetros (con parámetros default)
def generate_elections(n=500, seed=42, missing_rate=0.0, save_to=None, locale="en_US"):
    """
    Genera un conjunto de datos sintético de elecciones ficticias.
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
    candidates = ["Candidate A", "Candidate B", "Candidate C", "Candidate D"]
    parties = ["Progressive Party", "Conservative Party", "Green Party", "Liberal Party"]
    election_types = ["Presidential", "Legislative", "Municipal", "Regional"]
    # genera nombres de regiones usando Faker y divide entre el número de candidatos porque cada región generará una fila por candidato
    regions = [fake.state() for _ in range(n // len(candidates))]

    rows = [] # inicializa una lista vacía que irá llenando fila por fila
    for region in regions: # itera sobre cada región generada 
        total_votes = np.random.randint(10000, 500000) # genera el total de votos de la región entre 10,000 y 500,000 (1 solo número por región)
        raw = np.random.dirichlet(alpha=[3, 2, 1, 1]) * total_votes # genera 4 proporciones que usman exactamente 1 usando distribución Dirichlet, luego las múltiplica por el total de votos. alpha hace que el candidato A tenga ventaja sobre todos los demás (imitando realidad)
        votes_per_candidate = raw.astype(int) # convierte los votos a enteros (pequeña pérdida de precisión)

        for i, candidate in enumerate(candidates): # itera sobre cada candidato (el índice i se usa para asignar el partido correspondiente)
            rows.append({  # agrega una fila al listado
                "record_id": f"ELEC_{str(len(rows)).zfill(6)}", # genera ids únicos y secuenciales usando len(rows) como contador
                "region": region, 
                "election_type": np.random.choice(election_types), # escoge tipo de elección aleatoriamente con probabilidad uniforme
                "year": np.random.choice([2020, 2021, 2022, 2023, 2024]), # escoge año de elección con probabilidad uniforme
                "candidate": candidate,
                "party": parties[i],
                "votes": votes_per_candidate[i],
                "total_votes_region": total_votes,
                "turnout_pct": np.round(np.random.uniform(40, 85), 1), # genera participación electoral con distribución uniforme continua entre 40% y 85%
                "incumbent": candidate == "Candidate A", # marca al candidato A como incumbente
            })

    df = pd.DataFrame(rows[:n])
    
    # calcula el porcentaje de votos de cada candidato en su región
    df["vote_share_pct"] = np.round(df["votes"] / df["total_votes_region"] * 100, 2)

    if save_to: # guarda a csv o excel si se especifica
        export_data(df, save_to)    

    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)