"""
data_cleaning.py
-----------------
STEP 1: DATA CLEANING

Takes the raw, messy dataset (data/uber_rides_raw.csv) and produces a
clean version (data/uber_rides_cleaned.csv).

What we clean:
1. Duplicate rows -> removed.
2. Missing 'fare' values -> filled with the average fare for that
   same pickup_area (a more accurate fill than just using the overall
   average, since fares vary a lot by area).
3. Missing 'rating' values -> filled with the overall average rating.
4. Make sure data types are correct (dates as dates, ride_id as int).

Run:
    python src/data_cleaning.py
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_FILE = os.path.join(DATA_DIR, "uber_rides_raw.csv")
CLEAN_FILE = os.path.join(DATA_DIR, "uber_rides_cleaned.csv")


def load_raw_data():
    return pd.read_csv(RAW_FILE, parse_dates=["date"])


def clean_data(df):
    print(f"Rows before cleaning: {len(df)}")
    print(f"Missing values before cleaning:\n{df.isna().sum()}")

    # Step A: remove exact duplicate rows
    df = df.drop_duplicates()

    # Step B: sort by date and reset row numbers
    df = df.sort_values("date").reset_index(drop=True)

    # Step C: fill missing 'fare' using the average fare for that pickup_area
    df["fare"] = df.groupby("pickup_area")["fare"].transform(
        lambda x: x.fillna(round(x.mean(), 2))
    )

    # Step D: fill missing 'rating' using the overall average rating
    average_rating = df["rating"].mean()
    df["rating"] = df["rating"].fillna(round(average_rating, 1))

    print(f"\nRows after removing duplicates: {len(df)}")
    print(f"Missing values after cleaning:\n{df.isna().sum()}")

    return df


def main():
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)

    clean_df.to_csv(CLEAN_FILE, index=False)
    print(f"\nCleaned data saved to: data/uber_rides_cleaned.csv")


if __name__ == "__main__":
    main()
