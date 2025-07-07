import sqlite3
DB_PATH = 'complaints.db'
conn = sqlite3.connect('complaints.db')

def insert_complaint(name, hrms_id, department, category, description, date):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO complaints (name, hrms_id, department, category, description, date, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    ''', (name, hrms_id, department, category, description, date))

    conn.commit()
    conn.close()

def fetch_complaints():
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, hrms_id, department, category, description, date, status FROM complaints")
    complaints = cursor.fetchall()
    conn.close()
    return complaints


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
    
def track_status_by_hrms_id(hrms_id):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, description, status
        FROM complaints
        WHERE hrms_id = ?
    ''', (hrms_id,))
    result = cursor.fetchall()
    conn.close()
    return result

