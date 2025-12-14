import os
import sqlite3
from typing import Any

DB_FILENAME = "bokelai.db"


def get_db_connection() -> sqlite3.Connection:
    db_path = os.path.join(os.path.dirname(__file__), DB_FILENAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    schema_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publisher TEXT,
        price INTEGER NOT NULL,
        publish_date TEXT,
        isbn TEXT,
        cover_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """.strip()
    conn = get_db_connection()
    try:
        conn.execute(schema_sql)
        conn.commit()
    finally:
        conn.close()


def get_all_books(skip: int, limit: int) -> list[dict[str, Any]]:
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM books ORDER BY id LIMIT ? OFFSET ?",
            (limit, skip),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_book_by_id(book_id: int) -> dict[str, Any] | None:
    conn = get_db_connection()
    try:
        row = conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
        return dict(row) if row is not None else None
    finally:
        conn.close()


def create_book(
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> int:
    conn = get_db_connection()
    try:
        cur = conn.execute(
            """
            INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """.strip(),
            (title, author, publisher, price, publish_date, isbn, cover_url),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def update_book(
    book_id: int,
    title: str,
    author: str,
    publisher: str | None,
    price: int,
    publish_date: str | None,
    isbn: str | None,
    cover_url: str | None,
) -> bool:
    conn = get_db_connection()
    try:
        cur = conn.execute(
            """
            UPDATE books
            SET title = ?, author = ?, publisher = ?, price = ?, publish_date = ?, isbn = ?, cover_url = ?
            WHERE id = ?
            """.strip(),
            (title, author, publisher, price, publish_date, isbn, cover_url, book_id),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def delete_book(book_id: int) -> bool:
    conn = get_db_connection()
    try:
        cur = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
