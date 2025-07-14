import sqlite3
from src.data.scripts.connection import get_connection

def insert_audit_record(record: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_data (id, device_id, delta_value, accumulated_value, clasificacion, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        record['id'], record['device_id'], record['delta_value'],
        record['accumulated_value'], record['clasificacion'], record['timestamp']
    ))
    conn.commit()
    conn.close()

def insert_valid_record(record: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO valid_records (id, device_id, delta_value, accumulated_value, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        record['id'], record['device_id'], record['delta_value'],
        record['accumulated_value'], record['timestamp']
    ))
    conn.commit()
    conn.close()
