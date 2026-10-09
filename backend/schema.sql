PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS couple_info (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    nickname_a TEXT NOT NULL,
    nickname_b TEXT NOT NULL,
    anniversary TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diary_date TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    mood TEXT NOT NULL CHECK (mood IN ('happy', 'calm', 'sad', 'angry')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diary_photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diary_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (diary_id) REFERENCES diary(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS place (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    visited_date TEXT NOT NULL,
    diary_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (diary_id) REFERENCES diary(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS place_photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES place(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_diary_date ON diary(diary_date DESC);
CREATE INDEX IF NOT EXISTS idx_diary_mood ON diary(mood);
CREATE INDEX IF NOT EXISTS idx_place_visited_date ON place(visited_date DESC);
