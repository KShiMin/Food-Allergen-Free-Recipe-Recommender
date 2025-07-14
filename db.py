# db.py
import mariadb
import sys

def get_db_connection():
    try:
        return mariadb.connect(
            user="root",
            password="1234",
            host="127.0.0.1",
            port=3307,
            database="DatabaseProject"
        )
    except mariadb.Error as e:
        print(f"Connection error: {e}", file=sys.stderr)
        sys.exit(1)
