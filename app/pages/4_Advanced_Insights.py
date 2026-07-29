import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Advanced Insights", page_icon="📈", layout="wide")
st.title("📈 Advanced Insights & Clustering")

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

# Top 10
st.subheader("Top 10 Products with Highest Difference")
top10 = df.nlargest(10, "diff_percent")
fig = px.bar(top10, x="product", y="diff_percent", color="category", title="Top 10 Highest Gaps")
st.plotly_chart(fig, use_container_width=True)

# Clustering
st.subheader("Product Clustering (KMeans)")
features = df[["price_inr", "price_eur", "diff_percent"]]
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(scaled)

fig2 = px.scatter(df, x="price_inr", y="diff_percent", color="cluster",
                  hover_data=["product"], title="Product Clusters")
st.plotly_chart(fig2, use_container_width=True)