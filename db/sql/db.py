import sqlite3
import sys
from pathlib import Path

def get_db_connection():
    try:
        db_path = Path(__file__).resolve().parents[2] / "allergen-free-recipes.db"
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"SQLite Connection error: {e}", file=sys.stderr)
        sys.exit(1)
