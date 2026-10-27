import requests
import pandas as pd
import time
API_KEY = "YOUR_SERPAPI_KEY_HERE"

# Jin products/keywords ka data chahiye
KEYWORDS = ["iphone", "laptop", "shoes", "smartwatch", "headphones"]


def fetch_products_for_keyword(keyword, api_key):
    """Ek keyword ke liye Google Shopping se product list laata hai."""
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_shopping",
        "q": keyword,
        "api_key": api_key,
        "gl": "in",
        "hl": "en"
    }
    response = requests.get(url, params=params)
    data = response.json()

    products = []
    for item in data.get("shopping_results", []):
        products.append({
            "keyword": keyword,
            "position": item.get("position"),
            "title": item.get("title"),
            "price": item.get("price"),
            "extracted_price": item.get("extracted_price"),
            "rating": item.get("rating"),
            "reviews": item.get("reviews"),
            "platform": item.get("source"),
            "delivery": item.get("delivery"),
            "link": item.get("link"),
            "thumbnail": item.get("thumbnail"),
        })
    return products


def main():
    all_products = []
    for kw in KEYWORDS:
        print(f"Fetching data for keyword: {kw} ...")
        try:
            products = fetch_products_for_keyword(kw, API_KEY)
            all_products.extend(products)
            print(f"   -> {len(products)} products mile")
        except Exception as e:
            print(f"   -> Error: {e}")
        time.sleep(1)

    df = pd.DataFrame(all_products)
    df.to_csv("api_extracted_data.csv", index=False)
    print(f"\nDone! {len(df)} rows 'api_extracted_data.csv' me save hui.")


if __name__ == "__main__":
    main()
