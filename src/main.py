"""
main.py
-------
Runs the entire Uber Data Analysis pipeline in order:
1. Generate the dummy dataset (if not already generated)
2. Clean the data
3. Create visualizations
4. Run the analysis
5. Run the prediction model
6. Build the final dashboard

This is the single script you can run to reproduce every result and
every chart in this project from scratch.

Run:
    python src/main.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import generate_dataset
import data_cleaning
import visualize
import analysis
import predict
import dashboard


def section(title):
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)


def main():
    section("STEP 0: GENERATING DUMMY DATASET")
    generate_dataset.main()

    section("STEP 1: DATA CLEANING")
    data_cleaning.main()

    section("STEP 2: VISUALIZATION")
    visualize.main()

    section("STEP 3: ANALYSIS")
    analysis.main()

    section("STEP 4: PREDICTION MODEL")
    predict.main()

    section("STEP 5: DASHBOARD CREATION")
    dashboard.main()

    section("PIPELINE COMPLETE")
    print("All outputs have been saved to the output/ folder.")


if __name__ == "__main__":
    main()
