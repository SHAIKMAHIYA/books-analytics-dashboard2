import plotly.express as px

def price_histogram(df):
    return px.histogram(
        df, x="price", nbins=30,
        title="Price Distribution",
        template="plotly_white"
    )

def price_box(df):
    return px.box(
        df, y="price",
        title="Price Spread",
        template="plotly_white"
    )

def availability_bar(df):
    return px.bar(
        df.groupby("availability").price.mean().reset_index(),
        x="availability", y="price",
        title="Average Price by Availability",
        template="plotly_white"
    )

def segment_distribution(df):
    counts = df["segment"].value_counts().reset_index()
    counts.columns = ["segment", "count"]

    return px.bar(
        counts,
        x="segment",
        y="count",
        title="Books by Price Segment",
        color="segment",
        template="plotly_white"
    )

def segment_avg_price(df):
    avg = df.groupby("segment")["price"].mean().reset_index()

    return px.bar(
        avg,
        x="segment",
        y="price",
        title="Average Price by Segment",
        color="segment",
        template="plotly_white"
    )