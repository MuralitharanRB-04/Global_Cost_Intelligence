import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Overall Dashboard")

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

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", len(df))
col2.metric("Avg Difference", f"{df['diff_percent'].mean():.1f}%")
col3.metric("Highest Gap Category", df.groupby("category")["diff_percent"].mean().idxmax())
col4.metric("Lowest Gap Category", df.groupby("category")["diff_percent"].mean().idxmin())

# Main Scatter Plot
st.subheader("Overall Price Difference")
fig = px.scatter(
    df, x="product", y="diff_percent", color="category",
    size="price_diff_inr", hover_data=["price_inr", "price_eur"],
    title="% Higher in Ireland (Capped at 100%)", size_max=28
)
fig.update_layout(height=600, xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df[["product", "category", "price_inr", "price_eur", "diff_percent"]])