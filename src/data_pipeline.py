import pandas as pd
import os

def create_merged_dataset():
    """Load raw data, merge, engineer features, and save processed data."""
    india = pd.read_csv("data/india_prices.csv")
    ireland = pd.read_csv("data/ireland_prices.csv")

    df = pd.merge(india, ireland, on=["product", "category"], suffixes=("_in", "_ie"))

    # Feature Engineering
    df["price_ie_inr"] = df["price_eur"] * 90  # Approx conversion
    df["price_diff_inr"] = df["price_ie_inr"] - df["price_inr"]
    df["diff_percent"] = ((df["price_diff_inr"] / df["price_inr"]) * 100).clip(upper=100)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/merged_prices.csv", index=False)
    print("✅ Merged dataset created successfully!")
    return df

if __name__ == "__main__":
    create_merged_dataset()