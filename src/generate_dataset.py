"""
generate_dataset.py
--------------------
Creates a DUMMY Uber-style ride dataset. We generate our own data
instead of downloading from the internet so the project runs fully
offline.

Each row represents one ride, with columns:
- ride_id       : unique ID for the ride
- date          : date of the ride
- hour          : hour of day the ride started (0-23)
- pickup_area   : simulated pickup zone/neighborhood
- distance_km   : trip distance in kilometers
- fare          : total fare charged ($)
- passengers    : number of passengers
- rating        : rider's rating for the trip (1-5)

The data intentionally includes:
- a few missing values (blank cells)
- a few duplicate rows
so that the data_cleaning.py script has something real to clean.

Run:
    python src/generate_dataset.py
"""

import os
import random
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

PICKUP_AREAS = [
    "Downtown", "Airport", "Riverside", "Uptown", "Greenfield",
    "Old Town", "Tech Park", "Lakeside", "Hillcrest", "Market District"
]


def generate_rides(n_rides=500):
    dates = pd.date_range(start="2025-01-01", periods=90, freq="D")

    rows = []
    for i in range(1, n_rides + 1):
        date = random.choice(dates)

        # Rides are more common during morning/evening rush hours
        hour = int(np.clip(np.random.normal(loc=random.choice([8, 18]), scale=3), 0, 23))

        pickup_area = random.choice(PICKUP_AREAS)
        distance_km = round(abs(np.random.normal(loc=8, scale=5)) + 0.5, 2)

        # Fare roughly based on distance + a base fare + small random noise
        base_fare = 2.5
        per_km_rate = 1.3
        fare = round(base_fare + distance_km * per_km_rate + np.random.normal(0, 1.5), 2)
        fare = max(fare, 3.0)  # keep fares realistic (no negative/near-zero fares)

        passengers = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
        rating = random.choices([5, 4, 3, 2, 1], weights=[55, 25, 12, 5, 3])[0]

        rows.append({
            "ride_id": i,
            "date": date.strftime("%Y-%m-%d"),
            "hour": hour,
            "pickup_area": pickup_area,
            "distance_km": distance_km,
            "fare": fare,
            "passengers": passengers,
            "rating": rating
        })

    return pd.DataFrame(rows)


def make_it_messy(df):
    """Introduce a handful of missing values and duplicate rows on purpose."""
    df = df.copy()

    # Randomly blank out 'fare' or 'rating' in a few rows
    missing_indices = random.sample(range(len(df)), 12)
    for i in missing_indices:
        col = random.choice(["fare", "rating"])
        df.loc[i, col] = np.nan

    # Duplicate a few rows (simulates accidental double logging)
    duplicate_rows = df.sample(6, random_state=1)
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    return df


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    df = generate_rides()
    messy_df = make_it_messy(df)

    output_path = os.path.join(DATA_DIR, "uber_rides_raw.csv")
    messy_df.to_csv(output_path, index=False)

    print(f"Generated {len(messy_df)} rides (including intentional issues) -> data/uber_rides_raw.csv")
    print(f"Missing values introduced: {messy_df.isna().sum().sum()}")
    print(f"Duplicate rows introduced: {messy_df.duplicated().sum()}")


if __name__ == "__main__":
    main()
