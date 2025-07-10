import sqlite3
import uuid

DB_PATH = 'complaints.db'
conn = sqlite3.connect('complaints.db')

def generate_application_id():
    return "NWR-" + uuid.uuid4().hex[:8].upper()

def insert_complaint(name, hrms_id, department, category, description, date, file_path=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    application_id = generate_application_id()

    cursor.execute('''
        INSERT INTO complaints (name, hrms_id, department, category, description, date, status, application_id, file_path)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending', ?, ?)
    ''', (name, hrms_id, department, category, description, date, application_id, file_path))

    conn.commit()
    conn.close()
    return application_id


def fetch_complaints():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, hrms_id, department, category, description, date, status, application_id, file_path FROM complaints")
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
    
def track_status_by_app_id(application_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, department, category, description, date, status, file_path
        FROM complaints
        WHERE application_id = ?
    ''', (application_id,))
    result = cursor.fetchone()
    conn.close()
    return result


import sqlite3

def track_status_by_hrms_id(hrms_id):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT name, department, category, description, date, status, file_path
        FROM complaints
        WHERE TRIM(UPPER(hrms_id)) = ?
        ORDER BY date DESC
    ''', (hrms_id.strip().upper(),))

    results = cursor.fetchall()
    conn.close()
    return results



