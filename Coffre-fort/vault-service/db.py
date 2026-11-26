import sqlite3

DB_PATH = "/data/vault.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            owner_id TEXT NOT NULL,
            type  TEXT NOT NULL CHECK (type IN ('text', 'file')),
            enc_meta BLOB NOT NULL,
            meta_nonce BLOB NOT NULL,
            enc_data BLOB NOT NULL,
            data_nonce BLOB NOT NULL,
            size INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()