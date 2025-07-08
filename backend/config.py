# db_setup.py
import sqlite3
import pandas as pd

def create_table():
    import sqlite3
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        hrms_id TEXT NOT NULL,
        department TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        application_id TEXT UNIQUE,
        file_path TEXT  
    )
''')


    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
