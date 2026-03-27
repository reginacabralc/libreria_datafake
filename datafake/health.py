import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_health(n=500, seed=42):
    """
    Generate a synthetic health/patients dataset.

    Parameters
    ----------
    n : int
        Number of rows to generate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
    """
    np.random.seed(seed)
    Faker.seed(seed)

    diagnoses = ["Hypertension", "Diabetes", "Anxiety", "Depression", "Obesity",
                 "Asthma", "Arthritis", "Migraine", "Anemia", "None"]
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    specialties = ["General", "Cardiology", "Neurology", "Endocrinology", "Psychiatry", "Pediatrics"]

    df = pd.DataFrame({
        "patient_id": [f"PAT_{str(i).zfill(5)}" for i in range(1, n + 1)],
        "age": np.random.randint(1, 90, size=n),
        "gender": np.random.choice(["M", "F", "Other"], size=n, p=[0.48, 0.48, 0.04]),
        "blood_type": np.random.choice(blood_types, size=n),
        "weight_kg": np.round(np.random.normal(loc=70, scale=15, size=n).clip(30, 200), 1),
        "height_cm": np.round(np.random.normal(loc=168, scale=12, size=n).clip(100, 220), 1),
        "diagnosis": np.random.choice(diagnoses, size=n, p=[0.15, 0.12, 0.10, 0.10, 0.10,
                                                              0.08, 0.08, 0.07, 0.05, 0.15]),
        "specialty": np.random.choice(specialties, size=n),
        "num_consultations": np.random.poisson(lam=3, size=n),
        "smoker": np.random.choice([True, False], size=n, p=[0.20, 0.80]),
        "chronic_condition": np.random.choice([True, False], size=n, p=[0.35, 0.65]),
        "satisfaction_score": np.round(np.random.uniform(1, 10, size=n), 1),
        "visit_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n)],
    })

    df["bmi"] = np.round(df["weight_kg"] / (df["height_cm"] / 100) ** 2, 1)

    return df.reset_index(drop=True)