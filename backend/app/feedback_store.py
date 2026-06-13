import os
import sqlite3
from .config import settings


def _get_conn():
    db_path = settings.sqlite_path
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    return sqlite3.connect(db_path, check_same_thread=False)


def init_feedback_table():
    conn = _get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS message_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT NOT NULL,
                message_key TEXT NOT NULL,
                rating INTEGER NOT NULL,   -- 1 = thumbs up, -1 = thumbs down
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(thread_id, message_key)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_feedback(thread_id: str, message_key: str, rating: int):
    if rating not in (1, -1):
        raise ValueError("rating must be 1 or -1")

    conn = _get_conn()
    try:
        conn.execute(
            """
            INSERT INTO message_feedback (thread_id, message_key, rating)
            VALUES (?, ?, ?)
            ON CONFLICT(thread_id, message_key)
            DO UPDATE SET rating=excluded.rating, created_at=CURRENT_TIMESTAMP
            """,
            (thread_id, message_key, rating),
        )
        conn.commit()
    finally:
        conn.close()