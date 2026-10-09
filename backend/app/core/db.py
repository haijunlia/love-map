"""SQLite 数据库连接和运行目录管理。"""

from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
from typing import Iterator

BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_DIR / "data"
DB_PATH = Path(os.getenv("LOVE_MAP_DB", str(DATA_DIR / "love-map.db")))
UPLOAD_DIR = Path(os.getenv("LOVE_MAP_UPLOADS", str(BACKEND_DIR / "uploads")))


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    """创建数据目录、上传目录和数据库表。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    schema_path = BACKEND_DIR / "schema.sql"
    with _connect() as connection:
        connection.executescript(schema_path.read_text(encoding="utf-8"))
        connection.commit()


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    """为每个请求提供独立连接，并在异常时回滚。"""
    connection = _connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
