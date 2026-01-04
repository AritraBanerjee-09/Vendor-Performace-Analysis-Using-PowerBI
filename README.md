# 📊 Vendor Sales Performance Analysis

## 📌 Project Overview
This project analyzes **vendor sales performance** by integrating purchase, sales, pricing, and inventory data.  
The objective is to uncover insights related to **profitability, inventory efficiency, pricing behavior, and vendor contribution**, enabling data-driven business decisions.

The project follows a **complete data analytics lifecycle**:
- Data ingestion
- Data cleaning & transformation
- Exploratory Data Analysis (EDA)
- Statistical analysis
- Business insights & recommendations

---

## 🗂️ Dataset Description
The analysis is based on multiple relational tables stored in a SQLite database:

- **purchases** – Purchase transactions, quantities, and costs  
- **sales** – Sales revenue, quantities, and taxes  
- **purchase_prices** – Product pricing and volume details  
- **vendor_invoice** – Freight and vendor-level costs  

These datasets are merged to create a **vendor_sales_summary** table for analytics.

---

## 🛠️ Tech Stack & Tools
- **Programming Language:** Python  
- **Database:** SQLite  
- **Libraries Used:**
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scipy
  - sqlalchemy
- **Visualization:** Matplotlib & Seaborn  
- **Statistical Analysis:** SciPy  

---

## ⚙️ Project Structure
Vendor-Sales-Performance/
│
├── ingestion_db.py # Database ingestion logic
├── vendor_summary_pipeline.py # Main ETL & analysis pipeline
├── inventory.db # SQLite database
├── logs/
│ └── get_vendor_summary.log # Execution logs
├── requirements.txt # Project dependencies
└── README.md # Project documentation


---

## 🔄 Data Pipeline Workflow
1. **Data Ingestion**
   - CSV files ingested into SQLite
   - Tables created using SQLAlchemy

2. **Data Aggregation**
   - Vendor-level metrics computed using optimized SQL (CTEs)
   - Metrics include:
     - Total Sales
     - Total Purchases
     - Gross Profit
     - Profit Margin
     - Stock Turnover
     - Freight Cost

3. **Data Cleaning**
   - Missing values handled
   - Data types standardized
   - Vendor names cleaned for consistency

4. **Feature Engineering**
   - Gross Profit
   - Profit Margin (%)
   - Stock Turnover Ratio
   - Sales-to-Purchase Ratio
   - Unsold Inventory Value

---

## 📊 Exploratory Data Analysis (EDA)
The project includes multiple EDA visualizations:
- Distribution plots for numerical variables
- Box plots to detect outliers
- Count plots for top vendors and products
- Correlation heatmap for numerical features
- Bar charts for top vendors & brands
- Pareto analysis (80/20 rule)
- Donut chart for purchase contribution
- Scatter plots for sales vs profit margins

---

## 📈 Statistical Analysis
### Hypothesis Testing
**Question:**  
_Is there a significant difference in profit margins between top-performing and low-performing vendors?_

- **Null Hypothesis (H₀):**  
  No significant difference in mean profit margins
- **Alternative Hypothesis (H₁):**  
  Mean profit margins are significantly different

**Test Used:**  
Two-Sample T-Test (Welch’s t-test)

**Result:**  
The p-value indicates a **statistically significant difference**, confirming that **low-sales vendors tend to maintain higher profit margins**.

---

## 🔍 Key Insights
- Strong correlation between purchase quantity and sales quantity confirms **efficient inventory turnover**
- Low-performing vendors exhibit **higher profit margins**, likely due to premium pricing or lower costs
- High-performing vendors achieve volume but at **lower margins**
- Significant capital is locked in **unsold inventory** for specific vendors
- A small subset of vendors contributes to the majority of purchases (Pareto principle)

---

## 💡 Business Recommendations
- **High-Sales Vendors**
  - Optimize pricing strategies
  - Reduce operational costs
  - Explore bundling opportunities

- **Low-Sales Vendors**
  - Improve marketing and distribution
  - Reassess pricing competitiveness
  - Leverage strong margins for expansion

- **Inventory Management**
  - Reduce excess stock
  - Improve demand forecasting
  - Monitor capital locked in unsold inventory

---

## ▶️ How to Run the Project

### 1️⃣ Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows
