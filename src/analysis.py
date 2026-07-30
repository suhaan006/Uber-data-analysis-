"""
analysis.py
-----------
STEP 3: ANALYSIS

Calculates simple statistics that describe the ride data:
1. Total number of rides and total revenue
2. Average fare, average distance, average rating
3. Busiest hour of the day
4. Most popular pickup area
5. Correlation between distance and fare (do longer rides cost more?)

Run:
    python src/analysis.py
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "uber_rides_cleaned.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


def print_summary(df):
    print("=" * 55)
    print("UBER RIDE DATA - ANALYSIS SUMMARY")
    print("=" * 55)

    total_rides = len(df)
    total_revenue = df["fare"].sum()
    average_fare = df["fare"].mean()
    average_distance = df["distance_km"].mean()
    average_rating = df["rating"].mean()

    busiest_hour = df["hour"].value_counts().idxmax()
    most_popular_area = df["pickup_area"].value_counts().idxmax()

    # Correlation: how strongly distance and fare move together
    # (1.0 = perfectly together, 0 = no relationship)
    correlation = df["distance_km"].corr(df["fare"])

    print(f"Total rides            : {total_rides}")
    print(f"Total revenue          : ${total_revenue:,.2f}")
    print(f"Average fare           : ${average_fare:.2f}")
    print(f"Average distance       : {average_distance:.2f} km")
    print(f"Average rating         : {average_rating:.2f} / 5")
    print(f"Busiest hour           : {busiest_hour}:00")
    print(f"Most popular pickup    : {most_popular_area}")
    print(f"Distance-Fare correlation: {correlation:.3f} (closer to 1 = longer rides cost more, as expected)")
    print("=" * 55)

    return {
        "total_rides": total_rides,
        "total_revenue": total_revenue,
        "average_fare": average_fare,
        "average_distance": average_distance,
        "average_rating": average_rating,
        "busiest_hour": busiest_hour,
        "most_popular_area": most_popular_area,
        "correlation": correlation
    }


def save_summary_to_file(stats):
    lines = [
        "UBER RIDE DATA - ANALYSIS SUMMARY",
        f"Total rides: {stats['total_rides']}",
        f"Total revenue: ${stats['total_revenue']:,.2f}",
        f"Average fare: ${stats['average_fare']:.2f}",
        f"Average distance: {stats['average_distance']:.2f} km",
        f"Average rating: {stats['average_rating']:.2f} / 5",
        f"Busiest hour: {stats['busiest_hour']}:00",
        f"Most popular pickup area: {stats['most_popular_area']}",
        f"Distance-Fare correlation: {stats['correlation']:.3f}",
    ]

    with open(os.path.join(OUTPUT_DIR, "analysis_summary.txt"), "w") as f:
        f.write("\n".join(lines))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()

    stats = print_summary(df)
    save_summary_to_file(stats)
    print("\nSummary also saved to output/analysis_summary.txt")


if __name__ == "__main__":
    main()
