
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

DB_CONFIG = {
    "user": "root",
    "password": "YOUR_PASSWORD",
    "host": "localhost",
    "port": 3306,
    "database": "brand_visibility"
}


def load_data_from_mysql():
    connection_string = (
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(connection_string)
    df = pd.read_sql("SELECT * FROM products", engine)
    print(f"MySQL se data mil gaya. Shape: {df.shape}")
    return df


def main():
    df = load_data_from_mysql()
    os.makedirs("eda_charts", exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.histplot(df["price"], bins=30, kde=True, color="steelblue")
    plt.title("Price Distribution")
    plt.xlabel("Price")
    plt.savefig("eda_charts/01_price_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    df["brand"].value_counts().head(10).plot(kind="bar", color="orange")
    plt.title("Top 10 Brands by Product Count")
    plt.ylabel("Number of Products")
    plt.tight_layout()
    plt.savefig("eda_charts/02_brand_frequency.png")
    plt.close()
    plt.figure(figsize=(8, 5))
    df.groupby("brand")["visibility_score"].mean().sort_values(ascending=False).head(10).plot(
        kind="bar", color="green"
    )
    plt.title("Top 10 Brands by Avg Visibility Score")
    plt.tight_layout()
    plt.savefig("eda_charts/03_brand_visibility.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="position", y="price", alpha=0.5)
    plt.title("Price vs Ranking Position")
    plt.savefig("eda_charts/04_price_vs_position.png")
    plt.close()
   plt.figure(figsize=(8, 5))
    df["platform"].value_counts().plot(kind="bar", color="purple")
    plt.title("Products per Platform")
    plt.tight_layout()
    plt.savefig("eda_charts/05_platform_count.png")
    plt.close()


    plt.figure(figsize=(8, 5))
    df.groupby("platform")["rating"].mean().plot(kind="bar", color="brown")
    plt.title("Average Rating per Platform")
    plt.tight_layout()
    plt.savefig("eda_charts/06_platform_rating.png")
    plt.close()


    plt.figure(figsize=(8, 5))
    sns.histplot(df["position"], bins=20, color="teal")
    plt.title("Ranking Position Distribution")
    plt.savefig("eda_charts/07_position_distribution.png")
    plt.close()


    plt.figure(figsize=(8, 5))
    df.groupby("brand")["discount_pct"].mean().sort_values(ascending=False).head(10).plot(
        kind="bar", color="crimson"
    )
    plt.title("Top 10 Brands by Avg Discount %")
    plt.tight_layout()
    plt.savefig("eda_charts/08_discount_by_brand.png")
    plt.close()


    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="reviews", y="rating", alpha=0.5)
    plt.title("Rating vs Reviews")
    plt.savefig("eda_charts/09_rating_vs_reviews.png")
    plt.close()

    print("\nSaare 9 EDA charts 'eda_charts' folder me PNG images ke roop me save ho gaye hain!")
    print("Inko apni project report me daal sakte hain.")


if __name__ == "__main__":
    main()
