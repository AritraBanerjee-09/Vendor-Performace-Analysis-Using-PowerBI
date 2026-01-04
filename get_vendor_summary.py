import pandas as pd
import os
import sqlite3
import logging
import time
from sqlalchemy import create_engine
from ingestion_db import ingest_db

# --------------------------------------------------
# Logging setup
# --------------------------------------------------
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
    force=True
)

print("Logger initialized successfully")
logging.info("Logger initialized successfully")

# --------------------------------------------------
# Create Vendor Summary
# --------------------------------------------------
def create_vendor_summary(conn):
    """
    Merge purchase, sales, pricing, and freight data
    to generate vendor-level summary metrics.
    """

    start_time = time.time()
    print("Vendor summary query started at:", time.ctime(start_time))
    logging.info("Vendor summary query started")

    vendor_sales_summary = pd.read_sql_query(
        """
        WITH purchase_agg AS (
        SELECT
            VendorNumber,
            VendorName,
            Brand,
            Description,
            PurchasePrice,
            SUM(Quantity) AS TotalPurchaseQuantity,
            SUM(Dollars)  AS TotalPurchaseDollars
        FROM purchases
        WHERE PurchasePrice > 0
        GROUP BY
            VendorNumber,
            VendorName,
            Brand,
            Description,
            PurchasePrice
    ),


        sales_agg AS (
            SELECT
                VendorNo AS VendorNumber,
                Brand,
                SUM(SalesDollars)  AS TotalSalesDollars,
                SUM(SalesPrice)    AS TotalSalesPrice,
                SUM(SalesQuantity) AS TotalSalesQuantity,
                SUM(ExciseTax)     AS TotalExciseTax
            FROM sales
            GROUP BY
                VendorNo,
                Brand
        ),

        freight_agg AS (
            SELECT
                VendorNumber,
                SUM(Freight) AS FreightCost
            FROM vendor_invoice
            GROUP BY VendorNumber
        )

        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description, 
            p.PurchasePrice,

            pp.Volume,
            pp.Price AS ActualPrice,

            p.TotalPurchaseQuantity,
            p.TotalPurchaseDollars,

            COALESCE(s.TotalSalesDollars, 0)  AS TotalSalesDollars,
            COALESCE(s.TotalSalesPrice, 0)    AS TotalSalesPrice,
            COALESCE(s.TotalSalesQuantity, 0) AS TotalSalesQuantity,
            COALESCE(s.TotalExciseTax, 0)     AS TotalExciseTax,

            COALESCE(f.FreightCost, 0) AS FreightCost

        FROM purchase_agg p
        LEFT JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        LEFT JOIN sales_agg s
            ON p.VendorNumber = s.VendorNumber
           AND p.Brand = s.Brand
        LEFT JOIN freight_agg f
            ON p.VendorNumber = f.VendorNumber
        ORDER BY TotalSalesDollars DESC
        """,
        conn
    )

    end_time = time.time()
    print("Vendor summary query ended at:", time.ctime(end_time))
    print(f"Query execution time: {end_time - start_time:.2f} seconds")

    logging.info(f"Vendor summary query completed in {end_time - start_time:.2f} seconds")

    return vendor_sales_summary


# --------------------------------------------------
# Data Cleaning & Feature Engineering
# --------------------------------------------------
def clean_data(df):
    """
    Clean vendor summary data and create analytical metrics.
    """

    print("Cleaning data...")

    # Convert datatype
    df['Volume'] = df['Volume'].astype(float)

    # Fill missing values
    df.fillna(0, inplace=True)

    # Clean categorical columns
    df['VendorName'] = (
        df['VendorName']
        .astype(str)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    # Business metrics
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    df['ProfitMargin'] = (
        df['GrossProfit'] / df['TotalSalesDollars']
    ).where(df['TotalSalesDollars'] != 0, 0) * 100

    df['StockTurnover'] = (
        df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    ).where(df['TotalPurchaseQuantity'] != 0, 0)

    df['SalesToPurchaseRatio'] = (
        df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    ).where(df['TotalPurchaseDollars'] != 0, 0)

    print("Data cleaning completed")
    logging.info("Data cleaning completed")

    return df


# --------------------------------------------------
# Main Execution
# --------------------------------------------------
if __name__ == '__main__':

    print("Vendor summary pipeline started")
    logging.info("Vendor summary pipeline started")

    # READ connection
    conn = sqlite3.connect("inventory.db")

    print("Creating vendor summary...")
    summary_df = create_vendor_summary(conn)

    print("\nVendor Summary Preview:")
    print(summary_df.head())
    print("Rows:", len(summary_df))
    print("Columns:", summary_df.columns.tolist())

    print("\nCleaning vendor summary data...")
    clean_df = clean_data(summary_df)

    print("\nCleaned Data Preview:")
    print(clean_df.head())

    # IMPORTANT: close read connection before write
    conn.close()

    # WRITE engine
    engine = create_engine(
        "sqlite:///inventory.db",
        connect_args={"timeout": 30}
    )

    print("\nIngesting data into database...")
    logging.info("Ingesting data into vendor_sales_summary table")
    ingest_db(clean_df, "vendor_sales_summary", engine)

    print("Data ingested successfully into vendor_sales_summary")
    logging.info("Vendor summary pipeline completed successfully")

    print("Vendor summary pipeline completed successfully")
