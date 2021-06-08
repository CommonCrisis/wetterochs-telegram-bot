from datetime import datetime

import pandas as pd

from db.database import SQLite
from db.database import SQLitePandas


def fetch_data_to_df(table_name: str) -> pd.DataFrame:
    with SQLitePandas() as db:
        data = pd.read_sql_query(f'SELECT * FROM {table_name}', db)

    return data


def add_user(telegram_id: int, user_name: str):
    with SQLite() as cur:
        cur.execute(f"INSERT INTO users VALUES ('{telegram_id}', '{user_name}', NULL)")


def delete_user(telegram_id: int):
    with SQLite() as cur:
        cur.execute(f'DELETE FROM users WHERE telegram_id = {telegram_id}')


def update_user_hash(telegram_id: int, latest_hash: int):
    with SQLite() as cur:
        cur.execute(
            f"UPDATE users SET last_hash = '{latest_hash}' WHERE telegram_id = {telegram_id}",
        )


def add_hash(new_hash: str):
    with SQLite() as cur:
        cur.execute(f"INSERT INTO hashes VALUES ('{new_hash}', '{datetime.now()}')")
