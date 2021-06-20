import sqlite3

from utils.config import DB_BU_NAME
from utils.config import DB_NAME


class SQLite:
    def __init__(self, file=DB_NAME):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


class SQLitePandas:
    def __init__(self, file=DB_NAME):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def create_backup(context):
    con = sqlite3.connect(DB_NAME)
    bck = sqlite3.connect(DB_BU_NAME)
    with bck:
        con.backup(bck, pages=1)
    bck.close()
    con.close()
