# Brand Visibility Intelligence Dashboard
## Complete Beginner Guide — PyCharm + MySQL Workbench

Ye guide bilkul zero se shuru hoti hai. Maan ke chal rahe hain ki abhi
kuch bhi install nahi hai aapke laptop me.

---

# STEP 0: Software Install Karna (ek baar ka kaam)

## 0.1 — Python Install Karein
1. Jaayein: https://www.python.org/downloads/
2. "Download Python" button dabayein (latest version)
3. Installer khole → **"Add python.exe to PATH"** checkbox ZAROOR tick
   karein → phir "Install Now"

## 0.2 — PyCharm Install Karein
1. Jaayein: https://www.jetbrains.com/pycharm/download/
2. **Community Edition** (FREE) download karein
3. Installer chala ke default settings se install kar dein

## 0.3 — MySQL Server + MySQL Workbench Install Karein
1. Jaayein: https://dev.mysql.com/downloads/installer/
2. "MySQL Installer for Windows" download karein
3. Installer khole → **"Developer Default"** option choose karein
   (isme MySQL Server aur MySQL Workbench dono aa jaate hain)
4. Install karte waqt ek jagah aapko **root password set karne** ko
   kaha jayega — koi simple password rakh lein aur **ZAROOR YAAD RAKHEIN**
   (ye password baad me code me bhi likhna hoga)
5. Install poora hone ke baad, MySQL Workbench khol ke check karein ki
   "Local instance MySQL80" (ya jo naam ho) par double-click karke wahi
   password daalne se connect ho raha hai

> Mac/Linux use kar rahe hain? Same steps hain, bas installer
> https://dev.mysql.com/downloads/mysql/ se download karein.

---

# STEP 1: Project Folder Banana (PyCharm me)

1. PyCharm kholein → **"New Project"**
2. Location choose karein, jaise: `Documents/brand_visibility_project`
3. "Create" par click karein — PyCharm apna environment (venv) khud bana
   dega
4. Neeche jo saari `.py` files maine di hain (01 se 06 tak) aur
   `04_sql_queries.sql`, inko is project folder me copy kar dein
   (PyCharm me left-side "Project" panel me right-click → "Paste")

## 1.1 — Zaroori Libraries Install Karna
PyCharm ke neeche **"Terminal"** tab par click karein (bilkul neeche
dikhta hai), aur ye ek-ek karke ya sab ek saath chalayein:

```
pip install pandas numpy matplotlib seaborn requests sqlalchemy mysql-connector-python streamlit plotly
```

Isme thoda time lagega — ye normal hai.

---

# STEP 2: Dataset Haasil Karna

Aapko project PDF me diya gaya `brand_dirty_dataset.csv` link se
download karna hai, aur isko apne PyCharm project folder me daal dena hai
(wahi jaha baaki `.py` files hain).

Agar aap API se bhi data nikalna chahte hain (extra marks ke liye achha
hai), to `01_extract_api_data.py` file khole aur usme diye gaye
instructions follow karein (SerpApi free account chahiye hoga).

---

# STEP 3: MySQL me Database Banana (MySQL Workbench me)

1. MySQL Workbench kholein
2. Apne connection par double-click karein (password maangega, wahi
   daalein jo install ke waqt set kiya tha)
3. Upar ek **query editor tab** khula hoga — usme ye likhein:
   ```sql
   CREATE DATABASE brand_visibility;
   ```
4. Us line ko select karke **⚡ (lightning bolt icon)** dabayein, ya
   keyboard se `Ctrl + Enter` — isse database ban jayega
5. Neeche "Output" panel me "Action Output" green tick dikhega matlab
   success ho gaya

---

# STEP 4: Files Ko Order Se Run Karna (PyCharm me)

Har file ke andar bhi comments me poori detail likhi hai — lekin yaha
summary hai:

## File 1 — `01_extract_api_data.py` (OPTIONAL)
- **Kaha run karein**: PyCharm me file khol ke upar-right **green ▶️
  button** dabayein
- **Kya karti hai**: SerpApi se product data nikal ke `api_extracted_data.csv`
  banati hai
- Agar SerpApi account nahi hai, isko skip karein, seedha File 2 par jaayein

## File 2 — `02_clean_and_engineer.py`
- **Kaha run karein**: PyCharm green ▶️ button se
- **Kya karti hai**:
  - `brand_dirty_dataset.csv` (aur agar hai to `api_extracted_data.csv`)
    ko load karke merge karti hai
  - Missing values, galat data types, duplicates, outliers fix karti hai
  - Naye columns banati hai: `brand`, `visibility_score`, `price_range`,
    `discount_pct`
  - Final result `clean_brand_dataset.csv` me save karti hai
- **Output**: `clean_brand_dataset.csv` file ban jayegi

## File 3 — `03_load_to_mysql.py`
- **Pehle**: Isme upar `DB_CONFIG` dictionary me apna MySQL password
  daal dein:
  ```python
  DB_CONFIG = {
      "user": "root",
      "password": "YAHA_APNA_PASSWORD_DAALEIN",
      "host": "localhost",
      "port": 3306,
      "database": "brand_visibility"
  }
  ```
- **Kaha run karein**: PyCharm green ▶️ button se
- **Kya karti hai**: `clean_brand_dataset.csv` ko padh ke MySQL ke
  `brand_visibility` database me `products` naam ki table bana deti hai
- **Verify kaise karein**: MySQL Workbench me jaake likhein:
  ```sql
  USE brand_visibility;
  SELECT * FROM products LIMIT 10;
  ```
  Agar data dikhe, to sab sahi hua!

## File 4 — `04_sql_queries.sql`
- **Kaha run karein**: **MySQL Workbench me** (PyCharm me nahi!)
- MySQL Workbench me: **File → Open SQL Script** → is file ko select karein
- Isme 20+ ready-made queries hain jo project PDF ke "30 EDA Questions"
  ka jawab deti hain (jaise: sabse popular brand, sabse mehenga platform,
  discount analysis, etc.)
- Har query ko select karke `Ctrl + Enter` se ek-ek karke chalayein aur
  result dekh ke apni report me note kar lein

## File 5 — `05_eda_charts.py`
- **Pehle**: Isme bhi `DB_CONFIG` me apna password daal dein (File 3 jaisa hi)
- **Kaha run karein**: PyCharm green ▶️ button se
- **Kya karti hai**: MySQL se data leke 9 important graphs banati hai aur
  `eda_charts` folder me PNG images save karti hai
- Ye images aap apni project report me use kar sakte hain

## File 6 — `06_streamlit_dashboard.py`
- **Pehle**: `DB_CONFIG` me password daalein
- **Kaha run karein**: ⚠️ **PyCharm ke Terminal me** (green ▶️ button se
  NAHI!) Terminal me ye likhein:
  ```
  streamlit run 06_streamlit_dashboard.py
  ```
- Browser me automatically dashboard khul jayega
  (`http://localhost:8501`)
- Isme filters (Brand, Platform, Price) use karke dekh sakte hain

---

# STEP 5: Agar Error Aaye To

### "Can't connect to MySQL server"
- Check karein MySQL Server chal raha hai ya nahi: Windows me
  **Services** app kholein (Start menu me search karein) → "MySQL80"
  dhoondhe → agar "Running" nahi likha, right-click → "Start"

### "Access denied for user 'root'"
- Iska matlab `DB_CONFIG` me password galat hai — MySQL Workbench me
  jis password se login hota hai, wahi bilkul same yaha bhi daalein

### "ModuleNotFoundError: No module named 'pandas'" (ya kisi aur library ka)
- PyCharm Terminal me `pip install <library-name>` chalayein
- Dhyan rahe Terminal PyCharm ke andar ka hi ho (bottom tab), bahar ka
  Windows CMD nahi

### File 2 me "brand_dirty_dataset.csv nahi mili" message aaye
- Ye ek warning hai, error nahi — file khud practice ke liye ek sample
  dataset bana degi. Real result ke liye asli CSV file (PDF ke link se)
  download karke project folder me daal dein aur dobara run karein

---

# STEP 6: Submission Checklist

PDF ke hisaab se ye deliverables chahiye:

- [ ] **Source code** — saari `.py` files aur `.sql` file (GitHub par)
- [ ] **Clean dataset** — `clean_brand_dataset.csv`
- [ ] **Dashboard** — Streamlit app (`06_streamlit_dashboard.py`)
- [ ] **Project report** (Word/PDF) — Problem Statement, Approach, EDA
      insights (SQL queries ke results + charts), Business Insights
- [ ] **Screenshots** — dashboard ke, aur MySQL Workbench me chal rahi
      query results ke bhi
- [ ] **GitHub repository**

## GitHub par Upload Karna
1. https://github.com par account banayein, "New Repository" banayein
2. PyCharm ke Terminal me project folder ke andar hi:
   ```
   git init
   git add .
   git commit -m "Brand Visibility Intelligence Dashboard"
   git branch -M main
   git remote add origin <aapke-repo-ka-link>
   git push -u origin main
   ```

> ⚠️ Zaroor dhyan rakhein: `DB_CONFIG` me likha password GitHub par
> publicly na jaye. Upload karne se pehle password ko `"YOUR_PASSWORD"`
> jaisa placeholder wapas kar dein, ya better - password ko `.gitignore`
> me daali gayi ek alag `config.py` file me rakhein.

---

# Summary Table — Kya Kaha Chalega

| # | File | Kaha Run Karein |
|---|---|---|
| 1 | `01_extract_api_data.py` | PyCharm green ▶️ (optional) |
| 2 | `02_clean_and_engineer.py` | PyCharm green ▶️ |
| 3 | Create database | **MySQL Workbench** query editor |
| 4 | `03_load_to_mysql.py` | PyCharm green ▶️ |
| 5 | `04_sql_queries.sql` | **MySQL Workbench** (File → Open SQL Script) |
| 6 | `05_eda_charts.py` | PyCharm green ▶️ |
| 7 | `06_streamlit_dashboard.py` | **PyCharm Terminal**: `streamlit run 06_streamlit_dashboard.py` |

Order yehi follow karein, step by step. All the best! 🚀
