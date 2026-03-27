import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_elections(n=500, seed=42):
    """
    Generate a synthetic fictional elections dataset.

    Parameters
    ----------
    n : int
        Number of rows to generate (one row per region-candidate combination).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
    """
    np.random.seed(seed)
    Faker.seed(seed)

    candidates = ["Candidate A", "Candidate B", "Candidate C", "Candidate D"]
    parties = ["Progressive Party", "Conservative Party", "Green Party", "Liberal Party"]
    regions = [fake.state() for _ in range(n // len(candidates))]
    election_types = ["Presidential", "Legislative", "Municipal", "Regional"]

    rows = []
    for region in regions:
        total_votes = np.random.randint(10000, 500000)
        raw = np.random.dirichlet(alpha=[3, 2, 1, 1]) * total_votes
        votes_per_candidate = raw.astype(int)

        for i, candidate in enumerate(candidates):
            rows.append({
                "record_id": f"ELEC_{str(len(rows)).zfill(6)}",
                "region": region,
                "election_type": np.random.choice(election_types),
                "year": np.random.choice([2020, 2021, 2022, 2023, 2024]),
                "candidate": candidate,
                "party": parties[i],
                "votes": votes_per_candidate[i],
                "total_votes_region": total_votes,
                "turnout_pct": np.round(np.random.uniform(40, 85), 1),
                "incumbent": candidate == "Candidate A",
            })

    df = pd.DataFrame(rows[:n])
    df["vote_share_pct"] = np.round(df["votes"] / df["total_votes_region"] * 100, 2)

    return df.reset_index(drop=True)