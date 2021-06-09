import sqlite3


class SQLite:
    def __init__(self, file='telegram_bots.db.sqlite'):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


class SQLitePandas:
    def __init__(self, file='telegram_bots.db.sqlite'):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def create_backup(context):
    con = sqlite3.connect('telegram_bots.db.sqlite')
    bck = sqlite3.connect('telegram_bots_bkp.db.sqlite')
    with bck:
        con.backup(bck, pages=1)
    bck.close()
    con.close()
