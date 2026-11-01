import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "data" / "aura.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium',
            due_date TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def add_task(title, priority="Medium", due_date=""):
    with connect() as conn:
        conn.execute("INSERT INTO tasks(title,priority,due_date,status,created_at) VALUES(?,?,?,'Pending',?)",
                     (title, priority, due_date, now()))

def list_tasks(status=None):
    with connect() as conn:
        if status:
            return conn.execute("SELECT id,title,priority,due_date,status,created_at FROM tasks WHERE status=? ORDER BY id DESC", (status,)).fetchall()
        return conn.execute("SELECT id,title,priority,due_date,status,created_at FROM tasks ORDER BY id DESC").fetchall()

def update_task_status(task_id, status):
    with connect() as conn:
        conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))

def delete_task(task_id):
    with connect() as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))

def add_goal(title, description=""):
    with connect() as conn:
        conn.execute("INSERT INTO goals(title,description,created_at) VALUES(?,?,?)", (title, description, now()))

def list_goals():
    with connect() as conn:
        return conn.execute("SELECT id,title,description,created_at FROM goals ORDER BY id DESC").fetchall()

def add_memory(content):
    with connect() as conn:
        conn.execute("INSERT INTO memories(content,created_at) VALUES(?,?)", (content, now()))

def list_memories():
    with connect() as conn:
        return conn.execute("SELECT id,content,created_at FROM memories ORDER BY id DESC").fetchall()

def add_note(title, body):
    with connect() as conn:
        conn.execute("INSERT INTO notes(title,body,created_at) VALUES(?,?,?)", (title, body, now()))

def list_notes():
    with connect() as conn:
        return conn.execute("SELECT id,title,body,created_at FROM notes ORDER BY id DESC").fetchall()
