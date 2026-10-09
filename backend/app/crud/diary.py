"""日记相关数据库操作。"""

from datetime import date
import sqlite3
from typing import Any


def _photo_dict(row: sqlite3.Row) -> dict[str, Any]:
    path = row["file_path"]
    return {
        "id": row["id"],
        "file_path": path,
        "url": path,
        "sort_order": row["sort_order"],
    }


def _diary_dict(connection: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    photos = connection.execute(
        """
        SELECT id, file_path, sort_order
        FROM diary_photo
        WHERE diary_id = ?
        ORDER BY sort_order, id
        """,
        (row["id"],),
    ).fetchall()
    item = dict(row)
    item["photos"] = [_photo_dict(photo) for photo in photos]
    return item


def list_diaries(
    connection: sqlite3.Connection,
    mood: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict[str, Any]]:
    conditions = []
    params: list[Any] = []
    if mood:
        conditions.append("mood = ?")
        params.append(mood)
    if start_date:
        conditions.append("diary_date >= ?")
        params.append(start_date.isoformat())
    if end_date:
        conditions.append("diary_date <= ?")
        params.append(end_date.isoformat())

    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    rows = connection.execute(
        "SELECT id, diary_date, title, content, mood, created_at, updated_at "
        "FROM diary" + where + " ORDER BY diary_date DESC, id DESC",
        params,
    ).fetchall()
    return [_diary_dict(connection, row) for row in rows]


def get_diary(connection: sqlite3.Connection, diary_id: int) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT id, diary_date, title, content, mood, created_at, updated_at
        FROM diary WHERE id = ?
        """,
        (diary_id,),
    ).fetchone()
    return _diary_dict(connection, row) if row else None


def create_diary(connection: sqlite3.Connection, data: dict[str, Any]) -> dict[str, Any]:
    cursor = connection.execute(
        """
        INSERT INTO diary (diary_date, title, content, mood)
        VALUES (?, ?, ?, ?)
        """,
        (data["diary_date"], data["title"].strip(), data["content"].strip(), data["mood"]),
    )
    return get_diary(connection, cursor.lastrowid)


def update_diary(
    connection: sqlite3.Connection, diary_id: int, changes: dict[str, Any]
) -> dict[str, Any] | None:
    existing = get_diary(connection, diary_id)
    if not existing:
        return None

    allowed = {"diary_date", "title", "content", "mood"}
    updates = {key: value for key, value in changes.items() if key in allowed}
    if updates:
        if "title" in updates:
            updates["title"] = updates["title"].strip()
        if "content" in updates:
            updates["content"] = updates["content"].strip()
        updates["updated_at"] = "CURRENT_TIMESTAMP"
        assignments = []
        params = []
        for key, value in updates.items():
            if value == "CURRENT_TIMESTAMP":
                assignments.append(f"{key} = CURRENT_TIMESTAMP")
            else:
                assignments.append(f"{key} = ?")
                params.append(value)
        params.append(diary_id)
        connection.execute(
            "UPDATE diary SET " + ", ".join(assignments) + " WHERE id = ?",
            params,
        )
    return get_diary(connection, diary_id)


def add_photo(
    connection: sqlite3.Connection, diary_id: int, file_path: str
) -> dict[str, Any]:
    next_order = connection.execute(
        "SELECT COALESCE(MAX(sort_order), -1) + 1 FROM diary_photo WHERE diary_id = ?",
        (diary_id,),
    ).fetchone()[0]
    cursor = connection.execute(
        """
        INSERT INTO diary_photo (diary_id, file_path, sort_order)
        VALUES (?, ?, ?)
        """,
        (diary_id, file_path, next_order),
    )
    row = connection.execute(
        "SELECT id, file_path, sort_order FROM diary_photo WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()
    return _photo_dict(row)


def delete_diary(connection: sqlite3.Connection, diary_id: int) -> list[str] | None:
    existing = get_diary(connection, diary_id)
    if not existing:
        return None
    paths = [photo["file_path"] for photo in existing["photos"]]
    connection.execute("DELETE FROM diary WHERE id = ?", (diary_id,))
    return paths
