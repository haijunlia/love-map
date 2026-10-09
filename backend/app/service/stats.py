"""首页统计数据。"""

from datetime import date
import sqlite3


def _safe_anniversary(year: int, month: int, day: int) -> date:
    # 处理 2 月 29 日在非闰年不存在的情况。
    while day > 28:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1
    return date(year, month, day)


def get_stats(connection: sqlite3.Connection) -> dict:
    diary_count = connection.execute("SELECT COUNT(*) FROM diary").fetchone()[0]
    place_count = connection.execute("SELECT COUNT(*) FROM place").fetchone()[0]
    mood_rows = connection.execute(
        "SELECT mood, COUNT(*) AS count FROM diary GROUP BY mood ORDER BY mood"
    ).fetchall()

    couple = connection.execute(
        "SELECT anniversary FROM couple_info WHERE id = 1"
    ).fetchone()
    days_together = None
    next_anniversary_days = None
    if couple:
        anniversary = date.fromisoformat(couple["anniversary"])
        today = date.today()
        days_together = max(0, (today - anniversary).days)
        next_date = _safe_anniversary(today.year, anniversary.month, anniversary.day)
        if next_date < today:
            next_date = _safe_anniversary(
                today.year + 1, anniversary.month, anniversary.day
            )
        next_anniversary_days = (next_date - today).days

    return {
        "diary_count": diary_count,
        "place_count": place_count,
        "mood_distribution": [
            {"mood": row["mood"], "count": row["count"]} for row in mood_rows
        ],
        "days_together": days_together,
        "next_anniversary_days": next_anniversary_days,
    }
