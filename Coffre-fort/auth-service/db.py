import sqlite3

DB_PATH = "/data/auth.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            kdf_salt BLOB NOT NULL,
            kdf_params TEXT NOT NULL,
            auth_hash TEXT NOT NULL,
            wrapped_vault_key BLOB NOT NULL,
            wrap_nonce BLOB NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()