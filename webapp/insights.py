import pandas as pd
import numpy as np

def generate_insights(df: pd.DataFrame):
    insights = []

    total = len(df)
    avg_price = df["price"].mean()
    min_price = df["price"].min()
    max_price = df["price"].max()

    insights.append(
        f"📊 Dataset contains **{total} books** with prices ranging from **£{min_price:.2f} to £{max_price:.2f}**."
    )

    # Price distribution insight
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)

    mid_range_pct = ((df["price"].between(q1, q3)).mean()) * 100
    insights.append(
        f"📈 About **{mid_range_pct:.1f}%** of books are priced between **£{q1:.2f} and £{q3:.2f}**, indicating a strong mid-range concentration."
    )

    # Availability insight
    if "availability" in df.columns:
        in_stock_pct = (
            df["availability"].str.contains("In stock").mean() * 100
        )
        insights.append(
            f"📦 Only **{in_stock_pct:.1f}%** of books are currently in stock."
        )

    # Premium vs average comparison
    premium_threshold = df["price"].quantile(0.9)
    premium_avg = df[df["price"] >= premium_threshold]["price"].mean()

    insights.append(
        f"💰 Premium books (top 10%) are priced **{premium_avg / avg_price:.1f}× higher** than the average book."
    )

    # Outlier detection (IQR method)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    outliers = df[df["price"] > upper_bound]

    if len(outliers) > 0:
        insights.append(
            f"⚠️ Detected **{len(outliers)} price outliers**, which may represent rare or premium editions."
        )
    else:
        insights.append(
            "✅ No significant price outliers detected."
        )

    return insights
