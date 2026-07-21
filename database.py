import sqlite3


DATABASE_NAME = "tasks.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def seed_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Learn FastAPI", False)
        )

        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Build CRUD API", False)
        )

        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            ("Learn SQLite", False)
        )

    conn.commit()
    conn.close()