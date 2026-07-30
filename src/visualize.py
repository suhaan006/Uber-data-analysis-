"""
visualize.py
------------
STEP 2: VISUALIZATION

Creates simple, easy-to-read charts from the cleaned Uber rides data:
1. Number of rides by hour of day (shows rush hour patterns)
2. Number of rides by pickup area
3. Distribution of fares (histogram)
4. Average fare by pickup area

All charts are saved into the output/ folder as PNG images.

Run:
    python src/visualize.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "uber_rides_cleaned.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


def plot_rides_by_hour(df):
    rides_per_hour = df.groupby("hour").size().reindex(range(24), fill_value=0)

    plt.figure(figsize=(10, 5))
    rides_per_hour.plot(kind="bar", color="#4C72B0")
    plt.title("Number of Rides by Hour of Day")
    plt.xlabel("Hour (24-hour format)")
    plt.ylabel("Number of Rides")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "rides_by_hour.png"), dpi=150)
    plt.close()


def plot_rides_by_area(df):
    rides_per_area = df["pickup_area"].value_counts()

    plt.figure(figsize=(9, 5))
    rides_per_area.plot(kind="bar", color="#55A868")
    plt.title("Number of Rides by Pickup Area")
    plt.xlabel("Pickup Area")
    plt.ylabel("Number of Rides")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "rides_by_area.png"), dpi=150)
    plt.close()


def plot_fare_distribution(df):
    plt.figure(figsize=(8, 5))
    plt.hist(df["fare"], bins=20, color="#C44E52", edgecolor="black")
    plt.title("Distribution of Ride Fares")
    plt.xlabel("Fare ($)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fare_distribution.png"), dpi=150)
    plt.close()


def plot_average_fare_by_area(df):
    avg_fare = df.groupby("pickup_area")["fare"].mean().sort_values(ascending=False)

    plt.figure(figsize=(9, 5))
    avg_fare.plot(kind="bar", color="#8172B2")
    plt.title("Average Fare by Pickup Area")
    plt.xlabel("Pickup Area")
    plt.ylabel("Average Fare ($)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "average_fare_by_area.png"), dpi=150)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()

    plot_rides_by_hour(df)
    plot_rides_by_area(df)
    plot_fare_distribution(df)
    plot_average_fare_by_area(df)

    print("Charts saved to output/:")
    print(" - rides_by_hour.png")
    print(" - rides_by_area.png")
    print(" - fare_distribution.png")
    print(" - average_fare_by_area.png")


if __name__ == "__main__":
    main()
