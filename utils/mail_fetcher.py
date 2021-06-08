import hashlib
from typing import Tuple

import imgkit
import requests
from bs4 import BeautifulSoup


def _get_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    return soup


def fetch_overview():
    url_pic = 'https://www.wettermail.de/wetter/wettermail_inhalt.html'
    soup = _get_soup(url_pic)
    table = soup.find_all('table')[2]

    body = f"""
        <html>
        {table}
        </html>
    """
    options = {'format': 'png', 'encoding': 'UTF-8', 'xvfb': ''}

    imgkit.from_string(body, 'overview.png', options=options)


def fetch_mail_data() -> Tuple[str, int]:
    url_mail = 'https://www.wetterochs.de/wetter/current/wetter.html'
    soup = _get_soup(url_mail)
    msg = soup.find_all('body')[0].text

    msg_hash = int(hashlib.sha1(msg.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

    return msg, msg_hash


def fetch_data():
    fetch_overview()
    fetch_mail_data()


fetch_data()
