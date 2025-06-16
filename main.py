import sqlite3
import csv

def create_database():
    """Creates an SQLite database named 'data.db' and the transactions table."""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            TransactionID TEXT PRIMARY KEY,
            TransactionDateTime TEXT,
            StaffID TEXT,
            ItemID TEXT,
            ItemName_TH TEXT,
            ItemName_EN TEXT,
            Category TEXT,
            UnitPrice_THB REAL,
            Quantity INTEGER,
            TotalPrice_THB REAL,
            PaymentMethod TEXT,
            CustomerID TEXT,
            IsMember INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_data_from_csv(csv_file, db_file):
    """Inserts data from a CSV file into the 'transactions' table in the SQLite database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row

        # Adjust header names to be valid SQLite column names (e.g., remove spaces, parentheses)
        # ItemName (TH) -> ItemName_TH
        # ItemName (EN) -> ItemName_EN
        # UnitPrice_THB -> UnitPrice_THB (already good)
        # TotalPrice_THB -> TotalPrice_THB (already good)

        for row in reader:
            # Convert 'TRUE'/'FALSE' to 1/0 for IsMember
            row[12] = 1 if row[12].upper() == 'TRUE' else 0
            # Convert 'NULL' string to None for CustomerID
            row[11] = None if row[11].upper() == 'NULL' else row[11]

            cursor.execute('''
                INSERT INTO transactions (
                    TransactionID, TransactionDateTime, StaffID, ItemID, ItemName_TH,
                    ItemName_EN, Category, UnitPrice_THB, Quantity, TotalPrice_THB,
                    PaymentMethod, CustomerID, IsMember
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database 'data.db' created successfully.")
    insert_data_from_csv('data.csv', 'data.db')
    print("Data from 'data.csv' inserted into 'data.db' successfully.")
