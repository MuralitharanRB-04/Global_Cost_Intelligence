import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Category Analysis", page_icon="📂", layout="wide")
st.title("📂 Category-wise Analysis")

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

categories = df["category"].unique()
selected = st.selectbox("Select Category", categories)

cat_df = df[df["category"] == selected]

fig = px.bar(cat_df, x="product", y=["price_inr", "price_ie_inr"],
             barmode="group", title=f"{selected} – Price Comparison (₹)")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(cat_df[["product", "price_inr", "price_eur", "diff_percent"]])