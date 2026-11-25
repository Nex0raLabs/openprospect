"""Unified conversation storage and read APIs."""
from .db import connect, log

def ensure_schema():
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS conversations(
          id INTEGER PRIMARY KEY AUTOINCREMENT, channel TEXT NOT NULL,
          external_id TEXT NOT NULL UNIQUE, contact_address TEXT DEFAULT '',
          subject TEXT DEFAULT '', last_message TEXT DEFAULT '', unread INTEGER DEFAULT 0,
          status TEXT DEFAULT 'open', created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS conversation_messages(
          id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id INTEGER NOT NULL,
          direction TEXT NOT NULL, body TEXT NOT NULL, external_id TEXT DEFAULT '',
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE);
        """)
def list_conversations(limit=200):
    ensure_schema()
    with connect() as c:return [dict(x) for x in c.execute("SELECT * FROM conversations ORDER BY updated_at DESC,id DESC LIMIT ?",(limit,))]
def add_message(channel, external_id, address, subject, body, direction="inbound"):
    ensure_schema()
    with connect() as c:
        c.execute("INSERT OR IGNORE INTO conversations(channel,external_id,contact_address,subject,last_message,unread) VALUES(?,?,?,?,?,?)",(channel,external_id,address,subject,body[:12000],1 if direction=="inbound" else 0))
        row=c.execute("SELECT id FROM conversations WHERE external_id=?",(external_id,)).fetchone()
        if row:
            c.execute("INSERT INTO conversation_messages(conversation_id,direction,body,external_id) VALUES(?,?,?,?)",(row["id"],direction,body[:12000],external_id))
            c.execute("UPDATE conversations SET last_message=?,updated_at=CURRENT_TIMESTAMP,unread=? WHERE id=?",(body[:12000],1 if direction=="inbound" else 0,row["id"]))
    log("conversation_message",f"{channel} {direction} {address}")
