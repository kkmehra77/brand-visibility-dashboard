
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

st.set_page_config(page_title="Brand Visibility Intelligence Dashboard", layout="wide")

DB_CONFIG = {
    "user": "root",
    "password": "YOUR_PASSWORD",
    "host": "localhost",
    "port": 3306,
    "database": "brand_visibility"
}


@st.cache_data
def load_data():
    connection_string = (
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(connection_string)
    return pd.read_sql("SELECT * FROM products", engine)


df = load_data()

st.title("📊 Brand Visibility Intelligence Dashboard")
st.caption("E-commerce Analytics | Live data from MySQL")

st.sidebar.header("🔎 Filters")
brands = st.sidebar.multiselect("Brand", options=sorted(df["brand"].unique()))
platforms = st.sidebar.multiselect("Platform", options=sorted(df["platform"].unique()))
keywords = st.sidebar.multiselect("Keyword", options=sorted(df["keyword"].unique()))

min_price, max_price = float(df["price"].min()), float(df["price"].max())
price_range = st.sidebar.slider("Price Range", min_price, max_price, (min_price, max_price))

filtered_df = df.copy()
if brands:
    filtered_df = filtered_df[filtered_df["brand"].isin(brands)]
if platforms:
    filtered_df = filtered_df[filtered_df["platform"].isin(platforms)]
if keywords:
    filtered_df = filtered_df[filtered_df["keyword"].isin(keywords)]
filtered_df = filtered_df[
    (filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1])
]
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Brand Insights", "Pricing Analysis", "Product Explorer"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", len(filtered_df))
    col2.metric("Avg Price", f"₹{filtered_df['price'].mean():,.0f}")
    col3.metric("Avg Rating", f"{filtered_df['rating'].mean():.2f}")
    col4.metric("Total Reviews", f"{filtered_df['reviews'].sum():,.0f}")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(filtered_df, x="price", nbins=30, title="Price Distribution"), use_container_width=True)
    with c2:
        st.plotly_chart(px.pie(filtered_df, names="platform", title="Platform Share"), use_container_width=True)

with tab2:
    top_brand = filtered_df["brand"].value_counts().idxmax() if len(filtered_df) else "N/A"
    col1, col2 = st.columns(2)
    col1.metric("Top Brand", top_brand)
    col2.metric("Avg Visibility Score", f"{filtered_df['visibility_score'].mean():.3f}")

    c1, c2 = st.columns(2)
    with c1:
        bc = filtered_df["brand"].value_counts().reset_index()
        bc.columns = ["brand", "count"]
        st.plotly_chart(px.bar(bc.head(10), x="brand", y="count", title="Brand vs Product Count"), use_container_width=True)
    with c2:
        br = filtered_df.groupby("brand")["rating"].mean().reset_index().sort_values("rating", ascending=False)
        st.plotly_chart(px.bar(br.head(10), x="brand", y="rating", title="Brand vs Avg Rating"), use_container_width=True)

with tab3:
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Price", f"₹{filtered_df['price'].mean():,.0f}")
    col2.metric("Max Price", f"₹{filtered_df['price'].max():,.0f}")
    pct_disc = (filtered_df["discount_pct"] > 0).mean() * 100 if len(filtered_df) else 0
    col3.metric("% Discounted", f"{pct_disc:.1f}%")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.scatter(filtered_df, x="position", y="price", title="Price vs Ranking"), use_container_width=True)
    with c2:
        st.plotly_chart(px.scatter(filtered_df, x="rating", y="price", title="Price vs Rating"), use_container_width=True)

with tab4:
    search_term = st.text_input("🔍 Search by product title")
    table_df = filtered_df.copy()
    if search_term:
        table_df = table_df[table_df["title"].str.contains(search_term, case=False, na=False)]
    st.dataframe(
        table_df[["title", "brand", "price", "rating", "reviews", "platform", "position", "discount_pct"]].sort_values("position"),
        use_container_width=True
    )
