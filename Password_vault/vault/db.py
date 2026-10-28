import sqlite3
from pathlib import Path

DEFAULT_DB = Path.home() / ".vault.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    salt BLOB NOT NULL,
    check_token BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL UNIQUE,
    login TEXT NOT NULL,
    password_encrypted BLOB NOT NULL,
    url TEXT,
    tags TEXT NOT NULL DEFAULT '',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection(path=DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    
    