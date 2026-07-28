import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df))
col2.metric("Avg % Higher in Ireland", f"{df['diff_percent'].mean():.1f}%")
col3.metric("Most Expensive Category", df.groupby("category")["diff_percent"].mean().idxmax())

# Overall Scatter
st.subheader("Overall Price Difference Scatter Plot")
fig = px.scatter(
    df, x="product", y="diff_percent", color="category",
    size="price_diff_inr", title="% Higher in Ireland (capped at 100%)",
    hover_data=["price_inr", "price_eur"], size_max=25
)
fig.update_layout(height=550, xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Full Dataset")
st.dataframe(df[["product", "category", "price_inr", "price_eur", "diff_percent"]])