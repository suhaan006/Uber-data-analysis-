"""
predict.py
----------
STEP 4: PREDICTION MODEL

A BEGINNER-LEVEL model that predicts the FARE of a ride based on its
DISTANCE, using Linear Regression (fitting a straight line through
the data).

How it works, in plain terms:
1. We plot every ride as a point: (distance_km, fare).
2. We use numpy's polyfit function to find the straight line that
   best fits these points (same idea as "line of best fit" from
   school math - y = m*x + b).
3. We can now estimate the fare for any given distance, even ones not
   in our dataset.

Run:
    python src/predict.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "uber_rides_cleaned.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Example distances we'll predict fares for
SAMPLE_DISTANCES = [2, 5, 10, 15, 20]


def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=["date"])


def fit_fare_model(df):
    """
    Fits a straight line through (distance, fare) points.
    Returns the slope (m) and intercept (b) of fare = m*distance + b.
    """
    x = df["distance_km"].values
    y = df["fare"].values

    m, b = np.polyfit(x, y, deg=1)
    return m, b, x, y


def predict_fare(m, b, distance_km):
    return m * distance_km + b


def plot_model(df, x, y, m, b):
    plt.figure(figsize=(9, 6))
    plt.scatter(x, y, alpha=0.4, color="#4C72B0", label="Actual Rides")

    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = m * x_line + b
    plt.plot(x_line, y_line, color="#C44E52", linewidth=2, label="Fitted Line (Prediction Model)")

    plt.title("Fare Prediction Model: Fare vs Distance")
    plt.xlabel("Distance (km)")
    plt.ylabel("Fare ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fare_prediction_model.png"), dpi=150)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()

    m, b, x, y = fit_fare_model(df)
    print(f"Model equation: fare = {m:.3f} * distance_km + {b:.2f}")
    print(f"(This means each extra km adds about ${m:.2f} to the fare, on average)")

    print("\nSample fare predictions:")
    for distance in SAMPLE_DISTANCES:
        predicted_fare = predict_fare(m, b, distance)
        print(f"  Distance = {distance:>2} km  ->  Predicted Fare = ${predicted_fare:.2f}")

    plot_model(df, x, y, m, b)
    print("\nChart saved to output/fare_prediction_model.png")


if __name__ == "__main__":
    main()
