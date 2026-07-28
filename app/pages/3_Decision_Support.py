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

product = st.selectbox("Select Product", df["product"].unique())
row = df[df["product"] == product].iloc[0]

st.subheader(f"Analysis for: {product}")

col1, col2 = st.columns(2)
col1.metric("Price in India", f"₹{row['price_inr']:,.0f}")
col2.metric("Price in Ireland", f"€{row['price_eur']:.2f} (≈ ₹{row['price_ie_inr']:,.0f})")

st.success(f"**{row['diff_percent']:.1f}% more expensive in Ireland**")

if row["diff_percent"] > 70:
    st.warning("High difference → Prefer buying in India if possible (especially non-perishables).")
elif row["diff_percent"] > 40:
    st.info("Moderate difference → Compare quality and convenience before deciding.")
else:
    st.success("Low difference → Buy based on availability and preference.")