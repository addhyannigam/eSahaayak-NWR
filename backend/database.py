import sqlite3
DB_PATH = 'complaints.db'
conn = sqlite3.connect('complaints.db')

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
    cursor.execute("SELECT id, name, emp_id, email, category, description, date, status FROM complaints")
    data = cursor.fetchall()
    conn.close()
    return data

def update_status(complaint_id, new_status):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE id = ?", (new_status, complaint_id))
    conn.commit()
    conn.close()

def delete_complaint(cid):
    conn = sqlite3.connect('complaints.db') 
    c = conn.cursor()
    c.execute("DELETE FROM complaints WHERE id = ?", (cid,))
    conn.commit()
    conn.close()
    
def track_status_by_emp_id(emp_id):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, description, status
        FROM complaints
        WHERE emp_id = ?
    ''', (emp_id,))
    result = cursor.fetchall()
    conn.close()
    return result

