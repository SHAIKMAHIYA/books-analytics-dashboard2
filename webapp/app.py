import streamlit as st
import pandas as pd
from charts import price_histogram, price_box, availability_bar, segment_distribution, segment_avg_price
from insights import generate_insights
from utils import run_scraper, add_price_segment





st.set_page_config("Books Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("../data/books.csv")

df = load_data()
df = add_price_segment(df)
st.title("📚 Books Scraper & Analytics Platform")
tab_overview, tab_insights, tab_compare, tab_data = st.tabs(
    ["📊 Overview", "🧠 Insights", "⚖️ Compare", "📋 Data"]
)
with tab_overview:
    c1, c2, c3 = st.columns(3)
    c1.metric("Books", len(df))
    c2.metric("Avg Price", f"£{df.price.mean():.2f}")
    c3.metric("Max Price", f"£{df.price.max():.2f}")

    st.plotly_chart(price_histogram(df), use_container_width=True)
    st.plotly_chart(price_box(df), use_container_width=True)

# Sidebar
st.sidebar.header("Filters")
search = st.sidebar.text_input("Search book")
min_p, max_p = df.price.min(), df.price.max()
price = st.sidebar.slider("Price Range", float(min_p), float(max_p), (float(min_p), float(max_p)))

if search:
    df = df[df.title.str.contains(search, case=False)]

df = df[(df.price >= price[0]) & (df.price <= price[1])]
st.sidebar.divider()
st.sidebar.subheader("Data Control")

if st.sidebar.button("🔄 Refresh Data"):
    with st.spinner("Re-scraping latest data..."):
        run_scraper()
        st.cache_data.clear()
    st.success("Data refreshed successfully!")
    st.rerun()

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Books", len(df))
c2.metric("Avg Price", f"£{df.price.mean():.2f}")
c3.metric("Max Price", f"£{df.price.max():.2f}")

# Charts
st.plotly_chart(
    price_histogram(df),
    width="stretch",
    key="overview_hist"
)

st.plotly_chart(
    price_box(df),
    width="stretch",
    key="overview_box"
)

st.plotly_chart(
    availability_bar(df),
    width="stretch",
    key="overview_availability"
)

# Table + download
st.subheader("Data")
st.dataframe(df)
st.download_button("Download CSV", df.to_csv(index=False), "filtered_books.csv")

# Insights
with tab_insights:
    st.subheader("What does the data tell us?")
    insights = generate_insights(df)

    for i in insights:
        st.markdown(f"- {i}")
with tab_compare:
    st.subheader("Compare Price Segments")

    left, right = st.columns(2)

    with left:
        seg1 = st.selectbox("Select first segment", df["segment"].unique(), key="seg1")
    with right:
        seg2 = st.selectbox("Select second segment", df["segment"].unique(), key="seg2")

    df1 = df[df["segment"] == seg1]
    df2 = df[df["segment"] == seg2]

    c1, c2 = st.columns(2)
    c1.metric(f"{seg1} Avg Price", f"£{df1.price.mean():.2f}")
    c2.metric(f"{seg2} Avg Price", f"£{df2.price.mean():.2f}")

    st.plotly_chart(
    price_histogram(pd.concat([df1, df2])),
    width="stretch",
    key=f"compare_hist_{seg1}_{seg2}"
)

with tab_data:
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download filtered data",
        df.to_csv(index=False),
        "books_filtered.csv"
    )

# Price Segmentation
st.subheader("💸 Price Segmentation")

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
    segment_distribution(df),
    width="stretch",
    key="segment_dist"
)
   
with c2:
    st.plotly_chart(
    segment_avg_price(df),
    width="stretch",
    key="segment_avg"
)
    