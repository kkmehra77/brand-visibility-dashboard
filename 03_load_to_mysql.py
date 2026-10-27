import pandas as pd
from sqlalchemy import create_engine

DB_CONFIG = {
    "user": "root",                 # <-- MySQL Workbench me jo username use karte hain
    "password": "YOUR_PASSWORD",     # <-- apna MySQL root password
    "host": "localhost",             # <-- agar apne hi laptop par MySQL hai to "localhost"
    "port": 3306,                    # <-- MySQL ka default port
    "database": "brand_visibility"   # <-- ye database Workbench me pehle bana lein
}


def main():
    # Step 1: clean CSV padhna
    df = pd.read_csv("clean_brand_dataset.csv")
    print(f"'clean_brand_dataset.csv' load hui. Shape: {df.shape}")

    # Step 2: MySQL se connection banana
    connection_string = (
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(connection_string)

    # Step 3: DataFrame ko seedha SQL table me daal dena
    df.to_sql("products", engine, if_exists="replace", index=False)
    print(f"\nData MySQL database '{DB_CONFIG['database']}' me table 'products' ke naam se save ho gaya!")

    # Step 4: check karne ke liye ek chhoti query chala ke dikhate hain
    check = pd.read_sql("SELECT COUNT(*) AS total_rows FROM products;", engine)
    print("\nVerification query result:")
    print(check)

    print("\nAb MySQL Workbench me jaake 'SELECT * FROM products;' chalake khud dekh sakte hain.")


if __name__ == "__main__":
    main()
