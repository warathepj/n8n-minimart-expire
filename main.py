import sqlite3
import csv
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

PORT = 8000

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

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

def fetch_first_n_rows(db_file, num_rows):
    """Fetches and prints the first N rows from the 'transactions' table."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM transactions LIMIT {num_rows}')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_database()
    print("Database 'data.db' created successfully.")

    print("\nFetching first 3 rows from 'data.db':")
    first_3_rows = fetch_first_n_rows('data.db', 3)
    for row in first_3_rows:
        print(row)

    # Start the HTTP server
    os.chdir('.') # Ensure serving from the current directory
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving index.html at http://localhost:{PORT}")
        httpd.serve_forever()
