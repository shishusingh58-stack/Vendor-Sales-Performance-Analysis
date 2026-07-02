import sqlite3
import pandas as pd
import logging

# Logging Configuration

logging.basicConfig(
    filename="logs/vendor_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


# Database Connection


def create_connection(db_path: str):
    """
    Create SQLite database connection.

    db_path : str
        Path to SQLite database.

    """

    try:
        conn = sqlite3.connect(db_path)
        logging.info("Database connection established.")
        return conn

    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        raise


# Vendor Sales Summary Query


def fetch_vendor_sales_summary(conn) -> pd.DataFrame:
    """
    Generate vendor sales summary using SQL aggregations.

    conn : sqlite3.Connection

    """

    query = """
    WITH FreightSummary AS (
        SELECT VendorNumber,
               SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT p.VendorNumber,
               p.VendorName,
               p.Brand,
               p.PurchasePrice,
               pp.Volume,
               pp.Price AS ActualPrice,
               SUM(p.Quantity) AS TotalPurchaseQuantity,
               SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        GROUP BY p.VendorNumber, p.VendorName, p.Brand
    ),

    SalesSummary AS (
        SELECT VendorNo,
               Brand,
               SUM(SalesDollars) AS TotalSalesDollars,
               SUM(SalesQuantity) AS TotalSalesQuantity,
               SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT ps.*,
           ss.TotalSalesDollars,
           ss.TotalSalesQuantity,
           ss.TotalExciseTax,
           fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    """

    try:
        df = pd.read_sql_query(query, conn)
        logging.info("Vendor sales summary fetched successfully.")
        return df

    except Exception as e:
        logging.error(f"Query execution failed: {str(e)}")
        raise


# Data Cleaning


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform data quality corrections.

    Steps:
    - Type conversion
    - Missing value handling
    - Text normalization
    """

    logging.info("Starting data cleaning.")

    df['Volume'] = df['Volume'].astype('float64')
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()

    logging.info("Data cleaning completed.")

    return df


# Feature Engineering

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create analytical KPIs.

    KPIs:
    - Gross Profit
    - Profit Margin
    - Stock Turnover
    - Sales to Purchase Ratio
    """

    logging.info("Starting feature engineering.")

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    df['ProfitMargin'] = round(
        (df['GrossProfit'] / df['TotalSalesDollars'].replace(0, pd.NA)) * 100, 2
    )

    df['StockTurnover'] = round(
        df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'].replace(0, pd.NA), 4
    )

    df['SalestoPurchaseRatio'] = round(
        df['TotalSalesDollars'] / df['TotalPurchaseDollars'].replace(0, pd.NA), 3
    )

    logging.info("Feature engineering completed.")

    return df


# Save to database


def save_to_database(df: pd.DataFrame, conn, table_name: str):
    """
    Persist final dataset into database.
    """

    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        logging.info(f"Table '{table_name}' saved successfully.")

    except Exception as e:
        logging.error(f"Database write failed: {str(e)}")
        raise


# Main Pipeline


def main():

    conn = create_connection("inventory.db")

    df = fetch_vendor_sales_summary(conn)

    df = clean_data(df)

    df = engineer_features(df)

    save_to_database(df, conn, "VendorSalesSummary")

    conn.close()

    logging.info("Pipeline execution completed.")


if __name__ == "__main__":
    main()