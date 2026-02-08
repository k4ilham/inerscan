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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
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
