import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cost of Living", page_icon="🏠", layout="wide")
st.title("🏠 Cost of Living Index Estimator")

@st.cache_data
def load_data():
    india = pd.read_csv("data/india_prices.csv")
    ireland = pd.read_csv("data/ireland_prices.csv")
    df = pd.merge(india, ireland, on=["product", "category"], suffixes=("_in", "_ie"))
    df["price_ie_inr"] = df["price_eur"] * 90
    return df

df = load_data()

profile = st.selectbox("Select Your Profile", ["Student", "Working Professional", "Family of 3"])

# Simple weighted basket
weights = {
    "Student": {"Groceries": 0.5, "Electronics": 0.2, "Clothing": 0.15, "Personal Care": 0.15},
    "Working Professional": {"Groceries": 0.35, "Electronics": 0.3, "Clothing": 0.2, "Personal Care": 0.15},
    "Family of 3": {"Groceries": 0.55, "Electronics": 0.15, "Clothing": 0.15, "Personal Care": 0.15}
}

st.subheader(f"Estimated Monthly Basket for {profile}")

# Simplified calculation
avg_india = df["price_inr"].mean()
avg_ireland = df["price_ie_inr"].mean()

st.metric("Approx Monthly Cost in India", f"₹{avg_india * 25:,.0f}")
st.metric("Approx Monthly Cost in Ireland", f"€{(avg_ireland / 90) * 25:,.0f}")

st.info("This is a simplified estimate based on the current product basket.")