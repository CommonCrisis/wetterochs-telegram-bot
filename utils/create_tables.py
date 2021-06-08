from db.database import SQLite


def create_tables():
    with SQLite() as cur:
        cur.execute('DROP TABLE IF EXISTS users')
        cur.execute(
            'CREATE TABLE users (telegram_id INTEGER PRIMARY KEY, user_name VARCHAR, last_hash VARCHAR)',
        )
        cur.execute('DROP TABLE IF EXISTS hashes')
        cur.execute(
            'CREATE TABLE hashes (hash VARCHAR PRIMARY KEY, created_on TIMESTAMP)',
        )
