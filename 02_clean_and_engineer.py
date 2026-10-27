import pandas as pd
import numpy as np
import re
import os

def load_dirty_dataset(path="brand_dirty_dataset.csv"):
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"'{path}' load ho gayi. Shape: {df.shape}")
        return df
    else:
        print(f"'{path}' nahi mili is folder me!")
        print("-> PDF ke link se download karke is folder me daal dein.")
        print("-> Abhi practice ke liye ek SAMPLE (fake) dataset bana rahe hain.")
        return create_sample_dirty_dataset()


def load_api_dataset(path="api_extracted_data.csv"):
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"'{path}' load ho gayi. Shape: {df.shape}")
        return df
    else:
        print(f"'{path}' nahi mili — koi baat nahi, sirf dirty dataset se aage badhte hain.")
        return pd.DataFrame()


def create_sample_dirty_dataset(n=300):
    """Sirf PRACTICE ke liye nakli dataset — jab asli CSV mile to ye use hi nahi hoga."""
    np.random.seed(42)
    brands = ["Apple", "Samsung", "Boat", "OnePlus", "Sony", "Noise"]
    platforms = ["Amazon", "AMAZON", "flipkart", "Flipkart", "Myntra", "Walmart"]
    titles = [f"{np.random.choice(brands)} {np.random.choice(['Pro','Air','Max','Lite','Plus'])} !!!" for _ in range(n)]

    data = {
        "keyword": np.random.choice(["iphone", "laptop", "shoes", "smartwatch"], n),
        "position": np.random.randint(1, 60, n),
        "title": titles,
        "price": np.random.choice(["1999", "₹2,499", "Not Available", "3999", "0", "45999"], n),
        "raw_price": np.random.choice([2999, 5999, np.nan, 6999], n),
        "rating": np.random.choice([4.5, 3.9, np.nan, "many", 5.0], n),
        "reviews": np.random.choice([120, 45, np.nan, "many", 999], n),
        "platform": np.random.choice(platforms, n),
        "delivery": np.random.choice(["Free Delivery", "Paid", np.nan, "Prime"], n),
    }
    df = pd.DataFrame(data)
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)  # jaan-boojh kar duplicates
    return df


dirty_df = load_dirty_dataset()
api_df = load_api_dataset()


# =====================================================================
# 2.3  DATA MERGING (API + CSV)
# =====================================================================

def standardize_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

dirty_df = standardize_columns(dirty_df)

if not api_df.empty:
    api_df = standardize_columns(api_df)
    common_cols = list(set(dirty_df.columns) & set(api_df.columns))
    print(f"Common columns jo merge me use honge: {common_cols}")
    merged_df = pd.concat([dirty_df[common_cols], api_df[common_cols]], ignore_index=True)
else:
    merged_df = dirty_df.copy()

print(f"\nMerge hone ke baad shape: {merged_df.shape}")


# =====================================================================
# 2.4  DATA CLEANING (30 Data Cleaning Questions ka solution)
# =====================================================================

df = merged_df.copy()

print("\n--- Cleaning se pehle: Rows/Columns ---", df.shape)
print("Data types:\n", df.dtypes)
print("\nMissing values (%):\n", (df.isnull().mean() * 100).round(2))

def clean_price(value):
    """'₹2,499', 'Not Available' jaise messy price ko number me convert karta hai."""
    if pd.isna(value):
        return np.nan
    value = re.sub(r"[^\d.]", "", str(value))
    return float(value) if value != "" else np.nan

df["price"] = df["price"].apply(clean_price)
if "raw_price" in df.columns:
    df["raw_price"] = df["raw_price"].apply(clean_price)

def clean_numeric(value):
    """'many', 'N/A' jaise invalid text ko NaN banata hai, baaki ko number."""
    if pd.isna(value):
        return np.nan
    value = str(value).strip().lower()
    if value in ["many", "n/a", "not available", "-", ""]:
        return np.nan
    value = re.sub(r"[^\d.]", "", value)
    return float(value) if value != "" else np.nan

if "rating" in df.columns:
    df["rating"] = df["rating"].apply(clean_numeric)
if "reviews" in df.columns:
    df["reviews"] = df["reviews"].apply(clean_numeric)

# Missing price/rating/reviews -> median se fill
for col in ["price", "raw_price", "rating", "reviews"]:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Missing delivery -> "Unknown"
if "delivery" in df.columns:
    df["delivery"] = df["delivery"].fillna("Unknown")

# Duplicate rows hatana (title + price ke basis par)
before = len(df)
subset_cols = [c for c in ["title", "price"] if c in df.columns]
df = df.drop_duplicates(subset=subset_cols if subset_cols else None)
print(f"\nDuplicate rows hatai gayi: {before - len(df)}")

# Negative/zero price hatana
if "price" in df.columns:
    df = df[df["price"] > 0]

# Outliers CAP karna (IQR method)
if "price" in df.columns:
    Q1, Q3 = df["price"].quantile(0.25), df["price"].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = max(Q1 - 1.5 * IQR, 0), Q3 + 1.5 * IQR
    df["price"] = df["price"].clip(lower=lower, upper=upper)
    print(f"Price outliers cap kiye gaye {round(lower,2)} se {round(upper,2)} ke beech")

# Title clean karna (symbols/extra spaces hatana)
if "title" in df.columns:
    df["title"] = (
        df["title"].astype(str)
        .str.replace(r"[^a-zA-Z0-9\s]", "", regex=True)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

# Platform names standardize karna
if "platform" in df.columns:
    df["platform"] = df["platform"].astype(str).str.strip().str.title()

print("\n--- Cleaning ke baad missing values ---\n", df.isnull().sum())


# =====================================================================
# 2.5  FEATURE ENGINEERING
# =====================================================================

def extract_brand(title):
    if pd.isna(title) or title == "":
        return "Unknown"
    return str(title).split(" ")[0].title()

df["brand"] = df["title"].apply(extract_brand)

if "position" in df.columns:
    df["position"] = pd.to_numeric(df["position"], errors="coerce")
    df["position"] = df["position"].fillna(df["position"].median())
    df["visibility_score"] = round(1 / df["position"], 4)
else:
    df["visibility_score"] = np.nan

def price_bucket(p):
    if p < 1000:
        return "Budget (<1000)"
    elif p < 10000:
        return "Mid-Range (1000-10000)"
    elif p < 50000:
        return "Premium (10000-50000)"
    else:
        return "Luxury (50000+)"

df["price_range"] = df["price"].apply(price_bucket)

if "raw_price" in df.columns:
    df["discount_pct"] = np.where(
        df["raw_price"] > 0,
        round((df["raw_price"] - df["price"]) / df["raw_price"] * 100, 2),
        0
    )
    df["discount_pct"] = df["discount_pct"].clip(lower=0)
else:
    df["discount_pct"] = 0

print("\nNaye columns bane:", ["brand", "visibility_score", "price_range", "discount_pct"])
print(df.head())


# =====================================================================
# 2.6  FINAL CLEAN CSV SAVE KARNA (Deliverable)
# =====================================================================
df.to_csv("clean_brand_dataset.csv", index=False)
print("\n'clean_brand_dataset.csv' save ho gayi — ab File 3 (MySQL me load karna) chalayein.")
