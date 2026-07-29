import streamlit as st
import pandas as pd

st.set_page_config(page_title="Decision Support", page_icon="💡", layout="wide")
st.title("💡 Decision Support Engine")

@st.cache_data
def load_data():
    india = pd.read_csv("data/india_prices.csv")
    ireland = pd.read_csv("data/ireland_prices.csv")
    df = pd.merge(india, ireland, on=["product", "category"], suffixes=("_in", "_ie"))
    df["price_ie_inr"] = df["price_eur"] * 90
    df["price_diff_inr"] = df["price_ie_inr"] - df["price_inr"]
    df["diff_percent"] = ((df["price_diff_inr"] / df["price_inr"]) * 100).clip(upper=100)
    return df

df = load_data()

product = st.selectbox("Select a Product", df["product"].unique())
row = df[df["product"] == product].iloc[0]

st.subheader(f"Analysis: {product}")

c1, c2, c3 = st.columns(3)
c1.metric("India Price", f"₹{row['price_inr']:,.0f}")
c2.metric("Ireland Price", f"€{row['price_eur']:.2f}")
c3.metric("Difference", f"{row['diff_percent']:.1f}%")

st.progress(min(row["diff_percent"] / 100, 1.0))

if row["diff_percent"] >= 70:
    st.error("🔴 High Difference → Strongly prefer buying in India (if possible)")
elif row["diff_percent"] >= 40:
    st.warning("🟡 Moderate Difference → Compare quality, shipping & convenience")
else:
    st.success("🟢 Low Difference → Buy based on preference and availability")