import datetime
from os import getenv

import pandas as pd
import pytz
from dotenv import load_dotenv
from telegram.error import Unauthorized
from telegram.ext import CommandHandler
from telegram.ext import Updater

from crud.sql_queries import add_hash
from crud.sql_queries import add_user
from crud.sql_queries import delete_user
from crud.sql_queries import fetch_data_to_df
from crud.sql_queries import update_user_hash
from db.database import create_backup
from utils.config import WELCOME_MESSAGE
from utils.mail_fetcher import fetch_mail_data
from utils.mail_fetcher import fetch_overview


def start(update, context):
    add_user(update.effective_chat.id, update.effective_chat.full_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE)
    send_update(update, context)


def stop(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Schade, hab einen schönen Tag :)',
    )
    delete_user(update.effective_chat.id)


def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE)


def donate(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Hier kannst du dem WetterOchs einen Kaffee spendieren: https://www.wetterochs.de/wetter/sponsor/donation.html',
    )


def send_update(update, context):
    msg, msg_hash = fetch_mail_data()
    fetch_overview()

    try:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            parse_mode='HTML', text=msg,
        )
        with open('overview.png', 'rb') as pic:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic)

        update_user_hash(update.effective_chat.id, msg_hash)

    except Unauthorized:
        delete_user(update.effective_chat.id)


def send_wo_mail(context, users: pd.DataFrame) -> None:
    msg, msg_hash = fetch_mail_data()
    fetch_overview()

    user_ids = users[users['last_hash'] != str(msg_hash)]['telegram_id'].to_list()

    if user_ids:
        for user_id in user_ids:
            try:
                context.bot.send_message(chat_id=user_id, parse_mode='HTML', text=msg)
                with open('overview.png', 'rb') as pic:
                    context.bot.send_photo(chat_id=user_id, photo=pic)

                update_user_hash(user_id, msg_hash)

            except Unauthorized:
                delete_user(user_id)


def check_for_new_data(context):
    _, msg_hash = fetch_mail_data()

    hashes = fetch_data_to_df('hashes')['hash'].to_list()
    users = fetch_data_to_df('users')
    user_hashes = users['last_hash']

    has_latest = [True if p == str(msg_hash) else False for p in user_hashes]

    if not all(has_latest):
        if str(msg_hash) not in hashes:
            add_hash(msg_hash)
        send_wo_mail(context, users)


def run_telegram_bots():
    load_dotenv()

    updater = Updater(token=getenv('WO_BOT_TOKEN'))
    job_queue = updater.job_queue
    job_queue.run_repeating(check_for_new_data, interval=10)
    job_queue.run_daily(
        create_backup, datetime.time(
            hour=6, minute=27, tzinfo=pytz.timezone('Europe/Berlin'),
        ), days=(0, 1, 2, 3, 4, 5, 6),
    )

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)
    update_handler = CommandHandler('update', send_update)
    donate_handler = CommandHandler('donate', donate)
    info_handler = CommandHandler('info', info)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(update_handler)

    updater.start_polling()
    updater.idle()
