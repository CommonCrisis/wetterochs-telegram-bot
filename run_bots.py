from utils.config import REBUILD_TABLES
from utils.create_tables import create_tables
from utils.telegram_connector import run_telegram_bots

if __name__ == '__main__':
    if REBUILD_TABLES:
        create_tables()

    run_telegram_bots()
