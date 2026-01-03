import subprocess
import sys
import os
import pandas as pd

def add_price_segment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'segment' column based on price distribution.
    """
    df = df.copy()

    q_low = df["price"].quantile(0.30)
    q_high = df["price"].quantile(0.70)

    def segment_price(p):
        if p <= q_low:
            return "Budget"
        elif p <= q_high:
            return "Mid-range"
        else:
            return "Premium"

    df["segment"] = df["price"].apply(segment_price)
    return df

def run_scraper():
    """
    Runs the Scrapy spider to refresh books.csv
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    scraper_path = os.path.join(project_root, "scraper", "books_spider.py")

    subprocess.run(
        [sys.executable, "-m", "scrapy", "runspider", scraper_path],
        cwd=os.path.join(project_root, "scraper"),
        check=True
    )
