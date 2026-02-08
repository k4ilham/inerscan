import sqlite3
import os

class DatabaseService:
    def __init__(self, db_name="settings.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize the database and settings table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Scan history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                file_type TEXT,
                page_count INTEGER,
                file_size INTEGER,
                scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_scan_history(self, filename, filepath, file_type, page_count, file_size, notes=""):
        """Add a scan to history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scan_history (filename, filepath, file_type, page_count, file_size, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, filepath, file_type, page_count, file_size, notes))
        conn.commit()
        scan_id = cursor.lastrowid
        conn.close()
        return scan_id

    def get_scan_history(self, limit=50):
        """Get recent scan history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, filename, filepath, file_type, page_count, file_size, 
                   scan_date, notes
            FROM scan_history
            ORDER BY scan_date DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts
        history = []
        for row in results:
            history.append({
                'id': row[0],
                'filename': row[1],
                'filepath': row[2],
                'file_type': row[3],
                'page_count': row[4],
                'file_size': row[5],
                'scan_date': row[6],
                'notes': row[7]
            })
        return history

    def delete_scan_history(self, scan_id):
        """Delete a scan from history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM scan_history WHERE id = ?', (scan_id,))
        conn.commit()
        conn.close()

    def clear_scan_history(self):
        """Clear all scan history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM scan_history')
        conn.commit()
        conn.close()

    def get_setting(self, key, default=None):
        """Retrieve a setting value by key."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM app_settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else default

    def save_setting(self, key, value):
        """Save or update a setting value."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)
        ''', (key, str(value)))
        conn.commit()
        conn.close()
