"""地点相关数据库操作。"""

from typing import Any
import sqlite3


def _photo_dict(row: sqlite3.Row) -> dict[str, Any]:
    path = row["file_path"]
    return {
        "id": row["id"],
        "file_path": path,
        "url": path,
        "sort_order": row["sort_order"],
    }


def _place_dict(connection: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
    photos = connection.execute(
        """
        SELECT id, file_path, sort_order
        FROM place_photo
        WHERE place_id = ?
        ORDER BY sort_order, id
        """,
        (row["id"],),
    ).fetchall()
    item = dict(row)
    item["photos"] = [_photo_dict(photo) for photo in photos]
    return item


def list_places(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT p.id, p.name, p.latitude, p.longitude, p.visited_date,
               p.diary_id, p.created_at, d.title AS diary_title
        FROM place p
        LEFT JOIN diary d ON d.id = p.diary_id
        ORDER BY p.visited_date DESC, p.id DESC
        """
    ).fetchall()
    return [_place_dict(connection, row) for row in rows]


def get_place(connection: sqlite3.Connection, place_id: int) -> dict[str, Any] | None:
    row = connection.execute(
        """
        SELECT p.id, p.name, p.latitude, p.longitude, p.visited_date,
               p.diary_id, p.created_at, d.title AS diary_title
        FROM place p
        LEFT JOIN diary d ON d.id = p.diary_id
        WHERE p.id = ?
        """,
        (place_id,),
    ).fetchone()
    return _place_dict(connection, row) if row else None


def create_place(connection: sqlite3.Connection, data: dict[str, Any]) -> dict[str, Any]:
    cursor = connection.execute(
        """
        INSERT INTO place (name, latitude, longitude, visited_date, diary_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["name"].strip(),
            data["latitude"],
            data["longitude"],
            data["visited_date"],
            data.get("diary_id"),
        ),
    )
    return get_place(connection, cursor.lastrowid)


def update_place(
    connection: sqlite3.Connection, place_id: int, changes: dict[str, Any]
) -> dict[str, Any] | None:
    if not get_place(connection, place_id):
        return None
    allowed = {"name", "latitude", "longitude", "visited_date", "diary_id"}
    updates = {key: value for key, value in changes.items() if key in allowed}
    if updates:
        if "name" in updates:
            updates["name"] = updates["name"].strip()
        assignments = [f"{key} = ?" for key in updates]
        connection.execute(
            "UPDATE place SET " + ", ".join(assignments) + " WHERE id = ?",
            [*updates.values(), place_id],
        )
    return get_place(connection, place_id)


def add_photo(
    connection: sqlite3.Connection, place_id: int, file_path: str
) -> dict[str, Any]:
    next_order = connection.execute(
        "SELECT COALESCE(MAX(sort_order), -1) + 1 FROM place_photo WHERE place_id = ?",
        (place_id,),
    ).fetchone()[0]
    cursor = connection.execute(
        """
        INSERT INTO place_photo (place_id, file_path, sort_order)
        VALUES (?, ?, ?)
        """,
        (place_id, file_path, next_order),
    )
    row = connection.execute(
        "SELECT id, file_path, sort_order FROM place_photo WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()
    return _photo_dict(row)


def delete_place(connection: sqlite3.Connection, place_id: int) -> list[str] | None:
    existing = get_place(connection, place_id)
    if not existing:
        return None
    paths = [photo["file_path"] for photo in existing["photos"]]
    connection.execute("DELETE FROM place WHERE id = ?", (place_id,))
    return paths
