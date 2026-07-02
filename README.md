# Vendor-Sales-Performance-Analysis

## Problem Statement

In the retail industry, profitability is highly dependent on effective sales performance, inventory management, and vendor strategy. Inefficiencies in pricing, inventory turnover, and over-reliance on specific vendors can lead to revenue loss and increased operational costs.

This analysis aims to evaluate vendor and product performance using sales and purchase data to uncover inefficiencies, optimize procurement decisions, and improve overall profitability.

This project analyzes vendor-level purchasing and sales data to answer key business questions:

- Which brands need pricing adjustments having lower sales but higher profit margins?
- Which vendors and brands have the highest sales performance?
- How vendors contribute the most to total purchase?
- How much of the toal procurement is dependent on the top vendors?
- Does bulk purchasing reduce the unit price?
- Which vendors have low inventory turnover?
- How much capital is locked in unsold inventory?

The objective is to transform raw transactional data into actionable business insights using SQL, Python and analytical KPIs.

---

## Project Overview

This project simulates an end-to-end analytics workflow commonly used in industry:

1. **Raw Data → CSV Files**
2. **Data Ingestion → SQLite Database**
3. **Data Transformation → SQL + Python**
4. **Feature Engineering → Business KPIs**
5. **Visualization → Power BI Dashboard**
6. **Insights → Business Report**

---

## Dataset description

The dataset consists of retail inventory and vendor transactions:

- Purchases data
- Sales data
- Vendor invoices (freight costs)
- Purchase pricing information
- Inventory snapshots

Due to GitHub file size limitations, the full dataset and database files are not included.

A **sample dataset** is provided for demonstration purposes.

---

## Project Structure

``` bash
Vendor-Sales-Performance-Analysis/
│
├── Data_Ingestion.ipynb # Data ingestion notebook
├── Data_Ingestion.py # Data ingestion pipeline
│
├── Exploratory_Data_Analysis.ipynb # Initial data exploration
│
├── Vendor_Performance.ipynb # KPI computation notebook
├── Vendor_Performance_Pipeline.py # Modular analytics pipeline
│
├── VendorSalesSummary.csv # Final analytical dataset
│
├── Dashboard.pbix # Power BI Dashboard
├── Dashboard.pdf # Dashboard export
│
├── Final-Report.pdf # Business insights & conclusions
│
├── sample_data/ # Sample datasets (700 rows each)
│
├── Logs/ # Log files
│
├── generate_sample_data.py # Sample data generation script
│
├── README.md
├── LICENSE
```

--- 

## How to run the project

### Step 1 — Prepare the Data

Place the raw CSV files inside the `data/` directory.

For demonstration purposes, sample datasets are provided: 
`sample_data/`

You may copy these into the `data/` folder if you do not have the full dataset.

### Step 2 — Run Data Ingestion Pipeline

Execute the ingestion script:

```
python Data_Ingestion.py
```

This step will:
- Create the SQLite database (`inventory.db`)
- Ingest CSV files into database tables

### Step 3 - Run Vendor Performance Pipeline

Execute the anayltics pipeline:

```
python Vendor_Performance_Pipeline.py
```

This step will:
- Aggregate vendor-level metrics
- Perform data cleaning
- Compute analytical KPIs
- Generate the final dataset

---

## Analytical KPIs Computed

The pipeline derives key business metrics:
- Gross Profit
- Profit Margin
- Stock Turnover
- Sales-to-Purchase Ratio
- Freight Cost Impact

These metrics help evaluate:
-Vendor profitability
- Inventory efficiency
- Operational performance

---


## Dashboard and Visualization

Power BI dashboard included:

- Vendor Revenue Analysis
- Profitability Breakdown
- Inventory Efficiency Metrics
- Freight Cost Impact

Files:
- `Dashboard.pbix` → Interactive dashboard
- `Dashboard.pdf` → Static export

---

## Insights and Business Findings

All major business insights are documented in:
` Final-Report.pdf `

---

## Key skills demonstrated:

This project showcases:

- SQL (CTEs, Joins, Aggregations)
- Python (Pandas, ETL Pipelines)
- Data Cleaning & Transformation
- Feature Engineering (Business KPIs)
- Database Integration (SQLite)
- Data Visualization (Power BI)
- Logging & Pipeline Design

---

## Why This Project Matters

Vendor performance analysis is a core business analytics function in:

- Retail
- Supply Chain
- Inventory Management
- FMCG
- E-commerce

This project mirrors real-world analytics workflows used in industry.

---

## Notes

- Full dataset excluded due to GitHub size limits
- Sample datasets provided for reproducibility
- Database auto-generated via ingestion pipeline
