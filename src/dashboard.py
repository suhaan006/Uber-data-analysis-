"""
dashboard.py
------------
STEP 5: DASHBOARD CREATION

Combines the key charts into a single "dashboard" image with 4 panels,
so everything can be viewed at a glance in one picture:
1. Rides by hour of day
2. Rides by pickup area
3. Fare distribution
4. Fare prediction model (fare vs distance)

Run:
    python src/dashboard.py
(Best run after data_cleaning.py so the cleaned data already exists.)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "uber_rides_cleaned.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


def build_dashboard(df):
    rides_per_hour = df.groupby("hour").size().reindex(range(24), fill_value=0)
    rides_per_area = df["pickup_area"].value_counts()

    x = df["distance_km"].values
    y = df["fare"].values
    m, b = np.polyfit(x, y, deg=1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = m * x_line + b

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Uber Ride Data - Dashboard", fontsize=16, fontweight="bold")

    # Panel 1: Rides by hour
    axes[0, 0].bar(rides_per_hour.index, rides_per_hour.values, color="#4C72B0")
    axes[0, 0].set_title("Rides by Hour of Day")
    axes[0, 0].set_xlabel("Hour")
    axes[0, 0].set_ylabel("Number of Rides")

    # Panel 2: Rides by area
    axes[0, 1].bar(rides_per_area.index, rides_per_area.values, color="#55A868")
    axes[0, 1].set_title("Rides by Pickup Area")
    axes[0, 1].tick_params(axis="x", rotation=45)
    axes[0, 1].set_ylabel("Number of Rides")

    # Panel 3: Fare distribution
    axes[1, 0].hist(df["fare"], bins=20, color="#C44E52", edgecolor="black")
    axes[1, 0].set_title("Fare Distribution")
    axes[1, 0].set_xlabel("Fare ($)")
    axes[1, 0].set_ylabel("Frequency")

    # Panel 4: Fare prediction model
    axes[1, 1].scatter(x, y, alpha=0.4, color="#4C72B0", label="Actual")
    axes[1, 1].plot(x_line, y_line, color="#C44E52", linewidth=2, label="Prediction Line")
    axes[1, 1].set_title("Fare vs Distance (Prediction Model)")
    axes[1, 1].set_xlabel("Distance (km)")
    axes[1, 1].set_ylabel("Fare ($)")
    axes[1, 1].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUTPUT_DIR, "dashboard.png"), dpi=150)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    build_dashboard(df)
    print("Dashboard saved to output/dashboard.png")


if __name__ == "__main__":
    main()
