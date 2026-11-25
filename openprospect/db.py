from __future__ import annotations
import os, sqlite3
from pathlib import Path

def db_path() -> Path:
    home = Path(os.getenv("OPENPROSPECT_HOME", Path.home() / ".openprospect"))
    home.mkdir(parents=True, exist_ok=True)
    return home / "openprospect.db"

def connect():
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS companies (
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
      website TEXT DEFAULT '', industry TEXT DEFAULT '', location TEXT DEFAULT '',
      notes TEXT DEFAULT '', source TEXT DEFAULT 'manual',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS drafts (
      id INTEGER PRIMARY KEY AUTOINCREMENT, company_id INTEGER,
      channel TEXT DEFAULT 'email', subject TEXT DEFAULT '', body TEXT NOT NULL,
      status TEXT DEFAULT 'draft', created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(company_id) REFERENCES companies(id))""")
    conn.commit()
    return conn

def add_company(name, website="", industry="", location="", notes="", source="manual"):
    with connect() as c:
        cur=c.execute("INSERT INTO companies(name,website,industry,location,notes,source) VALUES(?,?,?,?,?,?)",
                      (name,website,industry,location,notes,source))
        return cur.lastrowid

def list_companies(limit=200):
    with connect() as c:
        return [dict(r) for r in c.execute("SELECT * FROM companies ORDER BY id DESC LIMIT ?",(limit,))]
