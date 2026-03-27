import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_music(n=500, seed=42):
    """
    Generate a synthetic music streaming dataset.

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

    genres = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz", "Classical", "Reggaeton", "R&B"]
    moods = ["Happy", "Sad", "Energetic", "Chill", "Romantic", "Angry"]
    platforms = ["Spotify", "Apple Music", "YouTube Music", "Tidal", "Deezer"]

    df = pd.DataFrame({
        "track_id": [f"TRK_{str(i).zfill(6)}" for i in range(1, n + 1)],
        "title": [fake.catch_phrase() for _ in range(n)],
        "artist": [fake.name() for _ in range(n)],
        "album": [fake.bs() for _ in range(n)],
        "genre": np.random.choice(genres, size=n, p=[0.25, 0.15, 0.20, 0.10, 0.05, 0.05, 0.12, 0.08]),
        "mood": np.random.choice(moods, size=n),
        "duration_seconds": np.random.randint(120, 360, size=n),
        "release_year": np.random.randint(1980, 2025, size=n),
        "streams": np.random.lognormal(mean=12, sigma=2, size=n).astype(int),
        "likes": np.random.lognormal(mean=8, sigma=2, size=n).astype(int),
        "platform": np.random.choice(platforms, size=n, p=[0.40, 0.25, 0.20, 0.08, 0.07]),
        "explicit": np.random.choice([True, False], size=n, p=[0.30, 0.70]),
        "bpm": np.random.randint(60, 180, size=n),
        "rating": np.round(np.random.uniform(1, 5, size=n), 1),
    })

    return df.reset_index(drop=True)