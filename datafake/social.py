import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_social(n=500, seed=42):
    """
    Generate a synthetic social media posts dataset.

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

    platforms = ["Instagram", "Twitter", "TikTok", "Facebook", "LinkedIn"]
    content_types = ["image", "video", "text", "story", "reel"]
    topics = ["Food", "Travel", "Tech", "Fashion", "Sports", "Music", "Politics", "Health"]

    df = pd.DataFrame({
        "post_id": [f"POST_{str(i).zfill(6)}" for i in range(1, n + 1)],
        "user_id": [f"USR_{str(np.random.randint(1, 201)).zfill(5)}" for _ in range(n)],
        "platform": np.random.choice(platforms, size=n, p=[0.30, 0.25, 0.20, 0.15, 0.10]),
        "content_type": np.random.choice(content_types, size=n, p=[0.30, 0.25, 0.20, 0.15, 0.10]),
        "topic": np.random.choice(topics, size=n),
        "date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(n)],
        "likes": np.random.lognormal(mean=5, sigma=2, size=n).astype(int),
        "comments": np.random.lognormal(mean=3, sigma=1.5, size=n).astype(int),
        "shares": np.random.lognormal(mean=2, sigma=1.5, size=n).astype(int),
        "reach": np.random.lognormal(mean=7, sigma=2, size=n).astype(int),
        "followers_at_post": np.random.lognormal(mean=8, sigma=2, size=n).astype(int),
        "is_viral": np.random.choice([True, False], size=n, p=[0.05, 0.95]),
    })

    df["engagement_rate"] = np.round(
        (df["likes"] + df["comments"] + df["shares"]) / df["reach"] * 100, 2
    )

    return df.reset_index(drop=True)