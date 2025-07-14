import sqlite3
from pathlib import Path

def initialize_database(
    db_path=None,
    schema_path=None
):
    if db_path is None:
        # ../.. from this file -> project root
        db_path = Path(__file__).resolve().parents[2] / "allergen-free-recipes.db"
    else:
        db_path = Path(db_path)

    if schema_path is None:
        schema_path = Path(__file__).parent / "project_sql_script_300625.sql"
    else:
        schema_path = Path(schema_path)

    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        sql_script = schema_path.read_text(encoding="utf-8")
        conn.executescript(sql_script)
        conn.commit()
        print(f"✅ Database initialized successfully at {db_path}")
    finally:
        conn.close()
