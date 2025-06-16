import sqlite3
import csv
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

PORT = 8000

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Fetch data from the database
            rows = fetch_first_n_rows('data.db', 10) # Fetching first 10 rows for example
            
            # Get column names from the cursor description
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items LIMIT 0') # Get schema without fetching data
            column_names = [description[0] for description in cursor.description]
            conn.close()

            # Convert rows to a list of dictionaries
            data = []
            for row in rows:
                data.append(dict(zip(column_names, row)))
            
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return
        elif self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

def fetch_first_n_rows(db_file, num_rows):
    """Fetches and prints the first N rows from the 'items' table."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM items LIMIT {num_rows}')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    print("\nFetching first 3 rows from 'data.db':")
    first_3_rows = fetch_first_n_rows('data.db', 3)
    for row in first_3_rows:
        print(row)

    # Start the HTTP server
    os.chdir('.') # Ensure serving from the current directory
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving index.html at http://localhost:{PORT}")
        httpd.serve_forever()
