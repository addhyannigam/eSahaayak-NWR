import sqlite3

def insert_complaint(name, emp_id, email, department, category, description, date):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO complaints (name, emp_id, email, department, category, description, date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
    ''', (name, emp_id, email, department, category, description, date))

    conn.commit()
    conn.close()

def fetch_complaints():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, emp_id, category, description, date, status FROM complaints")
    data = cursor.fetchall()
    conn.close()
    return data

def update_status(complaint_id, new_status):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE id = ?", (new_status, complaint_id))
    conn.commit()
    conn.close()
