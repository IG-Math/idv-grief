import sqlite3
from typing import List, Optional
from contextlib import contextmanager

DATABASE_NAME = "data.db"

@contextmanager
def get_db():
    """Context manager for database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize the database with tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create admin users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM data")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ("Sample Entry 1", "This is the first sample entry"),
                ("Sample Entry 2", "This is the second sample entry"),
                ("Sample Entry 3", "This is the third sample entry"),
            ]
            cursor.executemany(
                "INSERT INTO data (title, description) VALUES (?, ?)",
                sample_data
            )

def get_all_data() -> List[dict]:
    """Retrieve all data entries"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_data_by_id(data_id: int) -> Optional[dict]:
    """Retrieve a single data entry by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data WHERE id = ?", (data_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def create_data(title: str, description: str) -> int:
    """Create a new data entry"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO data (title, description) VALUES (?, ?)",
            (title, description)
        )
        return cursor.lastrowid

def update_data(data_id: int, title: str, description: str) -> bool:
    """Update an existing data entry"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE data SET title = ?, description = ? WHERE id = ?",
            (title, description, data_id)
        )
        return cursor.rowcount > 0

def delete_data(data_id: int) -> bool:
    """Delete a data entry"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data WHERE id = ?", (data_id,))
        return cursor.rowcount > 0

def get_admin_by_username(username: str) -> Optional[dict]:
    """Retrieve admin user by username"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

def create_admin(username: str, password_hash: str):
    """Create a new admin user"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
