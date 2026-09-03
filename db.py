import sqlite3
from datetime import date, datetime
from pathlib import Path
from models import Application, Status

DB_PATH = Path.home() / ".pipeline" / "pipeline.db"

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection):
    conn.execute(""" 
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL,
        source TEXT,
        link TEXT,
        date_applied TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        archived BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

def add_application(conn: sqlite3.Connection, app: Application) -> Application:
    cursor = conn.execute(
        """INSERT INTO applications 
        (company, role, status, source, link, date_applied, created_at, updated_at, archived)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (app.company, app.role, app.status.value, app.source, app.link, app.date_applied.isoformat(), app.created_at.isoformat(),
        app.updated_at.isoformat(), app.archived)
    )
    conn.commit()
    app.id = cursor.lastrowid
    return app

def list_applications(conn: sqlite3.Connection) -> list[Application]:
    rows = conn.execute("SELECT * FROM applications ORDER BY updated_at DESC").fetchall()
    return [_row_to_application(row) for row in rows]

def _row_to_application(row: sqlite3.Row) -> Application:
    return Application(
        id=row["id"],
        company=row["company"],
        role=row["role"],
        status=Status(row["status"]),
        source=row["source"],
        link=row["link"],
        date_applied=date.fromisoformat(row["date_applied"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
        archived=bool(row["archived"])
        )

def update_status(conn: sqlite3.Connection, application_id: int, new_status: Status) -> Application:
    conn.execute(
        """
        UPDATE applications
        SET updated_at = ?,
        status = ?
        WHERE id = ? """,
        (new_status.value, datetime.now().isoformat(), application_id)

    )
    conn.commit()
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()
    return _row_to_application(row)

def archive_application(conn: sqlite3.Connection, application_id: int):
    conn.execute(
        """
        UPDATE applications
        SET archived = 1, 
        updated_at = ?,
        where id = ? """,
        (datetime.now().isoformat(), application_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()
    return _row_to_application(row)
    