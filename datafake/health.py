import pandas as pd
import numpy as np
from faker import Faker
from .utils import inject_missing, export_data, inject_noise

# define la función con 5 parámetros (con parámetros default)
def generate_health(n=500, seed=42, missing_rate=0.0, save_to=None, locale="en_US", noise_level=0.0):
    """
    Genera un conjunto de datos sintético de salud/pacientes.
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
    diagnoses = ["Hypertension", "Diabetes", "Anxiety", "Depression", "Obesity",
                 "Asthma", "Arthritis", "Migraine", "Anemia", "None"]
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    specialties = ["General", "Cardiology", "Neurology", "Endocrinology", "Psychiatry", "Pediatrics"]

    df = pd.DataFrame({
        "patient_id": [f"PAT_{str(i).zfill(5)}" for i in range(1, n + 1)], # genera ids únicos tipo PAT_00001
        "age": np.random.randint(1, 91, size=n), # genera edades entre 1 y 90 con distribución uniforme discreta
        "gender": np.random.choice(["M", "F", "Other"], size=n, p=[0.48, 0.48, 0.04]), # escoge género con probabilidades iguales para M y F y con 4% para other
        "blood_type": np.random.choice(blood_types, size=n), # escoge tipo sanguíneo con probabilidad uniforme
        "weight_kg": np.round(np.random.normal(loc=70, scale=15, size=n).clip(30, 200), 1), # genera peso con distribución normal centrada en 70kg y variación de 15kg (.clip evita valores imposibles)
        "height_cm": np.round(np.random.normal(loc=168, scale=12, size=n).clip(100, 220), 1), # genera altura con distribución normal centrada en 168cm (promedio global ente hombres y mujeres)
        "diagnosis": np.random.choice(diagnoses, size=n, p=[0.15, 0.12, 0.10, 0.10, 0.10, 
                                                              0.08, 0.08, 0.07, 0.05, 0.15]), # escoge diagnóstico con probabilidades no uniformes basada en prevalencia aproximada
        "specialty": np.random.choice(specialties, size=n), # escoge especialidad con probabilidad uniforme
        "num_consultations": np.random.poisson(lam=3, size=n), # genera número de consultas con distribución poisson (modela conteos de eventos discretos en el tiempo) con promedio de 3 consultas por paciente
        "smoker": np.random.choice([True, False], size=n, p=[0.20, 0.80]), # genera con distribución Bernoulli, 20% fumadores (imitando tasas de tabaquismo en países desarrollados)
        "chronic_condition": np.random.choice([True, False], size=n, p=[0.35, 0.65]), # genera con distribución Bernoulli, 35% condición crónica
        "satisfaction_score": np.round(np.random.uniform(1, 10, size=n), 1), # genera calificación de satisfacción entre 1.0 y 10.0 con distribución unfirome continua (las encuestas de satisfacción tienden a evitar extremos)
        "visit_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n)], # genera fechas de visita en los últimos 2 años usando Faker
    })

    # Calcula el índice de masa corporal con la fórmula oficial
    df["bmi"] = np.round(df["weight_kg"] / (df["height_cm"] / 100) ** 2, 1)

    if save_to: # guarda a csv o excel si se especifica
        export_data(df, save_to)

    df = inject_noise(df, noise_level=noise_level, seed=seed) # inyecta ruido antes de los missing para que los NaNs también puedan aparecer en valores ruidosos
    
    # pasa el DataFrame completo por inject_missing antes de devolverlo
    return inject_missing(df, missing_rate=missing_rate, seed=seed)