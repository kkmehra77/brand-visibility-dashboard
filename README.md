# Brand Visibility Intelligence Dashboard

E-commerce analytics project: Google Shopping product data ka analysis
brand ranking, pricing aur platform competition par.

## Tools Used
Python (pandas, matplotlib, seaborn), MySQL, Streamlit, EDA

## Project Steps
1. Data extraction (SerpApi) aur CSV merging
2. Data cleaning aur feature engineering (brand, visibility_score, price_range, discount_pct)
3. MySQL me data storage
4. SQL queries se EDA
5. Python charts (matplotlib/seaborn)
6. Streamlit dashboard

## How to Run
1. pip install pandas numpy matplotlib seaborn requests sqlalchemy mysql-connector-python streamlit plotly
2. python 02_clean_and_engineer.py
3. MySQL me database banao: CREATE DATABASE brand_visibility;
4. python 03_load_to_mysql.py (apna MySQL password DB_CONFIG me daalo)
5. python 05_eda_charts.py
6. streamlit run 06_streamlit_dashboard.py

## Author
Kirpal
