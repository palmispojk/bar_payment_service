import sqlite3
import csv

def count_all_sales_items(db_path: str, start_date: str, end_date: str):
    """
    Count sales for all drinks and specials in a given date range.

    - Regular drinks: sum quantities as usual
    - Specials: count how many times each special deal was sold (not expanded into single drinks)

    Args:
        db_path (str): Path to the SQLite database.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        dict: { "Beer": 42, "Shot": 17, "Special: Shot x10": 8, ... }
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Count normal drinks
    cur.execute("""
        SELECT d.name, SUM(oi.quantity)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN drinks d ON oi.drink_id = d.id
        WHERE DATE(o.timestamp) BETWEEN DATE(?) AND DATE(?)
        GROUP BY d.name
    """, (start_date, end_date))
    drink_results = dict(cur.fetchall())

    # Count specials (number of deals sold, not multiplied by included drinks)
    cur.execute("""
        SELECT 'Special: ' || d.name || ' x' || s.quantity, COUNT(*)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN specials s ON oi.special_price_id = s.id
        JOIN drinks d ON s.drink_id = d.id
        WHERE DATE(o.timestamp) BETWEEN DATE(?) AND DATE(?)
        GROUP BY s.drink_id, s.quantity
    """, (start_date, end_date))
    special_results = dict(cur.fetchall())

    con.close()

    # Merge results
    all_results = {**drink_results, **special_results}
    return all_results



def total_revenue(db_path: str, start_date: str, end_date: str) -> float:
    """
    Sum all revenue from orders in the given date range.

    Args:
        db_path (str): Path to the SQLite database.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        float: Total revenue across all orders in the period.
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(total_price), 0)
        FROM orders
        WHERE DATE(timestamp) BETWEEN DATE(?) AND DATE(?)
    """, (start_date, end_date))

    total = cur.fetchone()[0]
    con.close()
    return total


def export_counts_and_total_to_csv(counts: dict, total: float, csv_file: str):
    """
    Write counts per item and total revenue to a CSV.

    Args:
        counts (dict): e.g., {'Beer': 42, 'Shot': 17, 'Special: Shot x10': 8}
        total (float): total revenue
        csv_file (str): output CSV path
    """
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(["Item", "Quantity Sold"])
        # Write counts
        for item, qty in counts.items():
            writer.writerow([item, qty])
        # Blank line and total
        writer.writerow([])
        writer.writerow(["TOTAL REVENUE", total])


if __name__ == "__main__":
    from env import DB_FILE_PATH, PROJECT_ROOT
    import os
    start = "2025-09-20"
    end = "2025-09-21"
    sales_items = count_all_sales_items(DB_FILE_PATH, start, end)
    print(sales_items)
    
    total = total_revenue(DB_FILE_PATH, start, end)
    print(total)
    
    analytics_folder = os.path.join(PROJECT_ROOT, "analytics")
    analytics_for_day = os.path.join(analytics_folder, start+"_"+end+".csv")
    export_counts_and_total_to_csv(sales_items, total, analytics_for_day)
    

    
    
