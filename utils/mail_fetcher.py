import hashlib
from typing import Tuple

import pandas as pd
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
from plotly.subplots import make_subplots


def _get_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    return soup


def fetch_overview() -> None:
    url_pic = 'https://www.wettermail.de/wetter/wettermail_inhalt.html'
    soup = _get_soup(url_pic)
    table = soup.find_all('table')[2]

    body = f"""
        <html>
        {table}
        </html>
    """
    create_plot(body)


def fetch_mail_data() -> Tuple[str, int]:
    url_mail = 'https://www.wetterochs.de/wetter/current/wetter.html'
    soup = _get_soup(url_mail)
    msg = soup.find_all('body')[0].text

    msg_hash = int(hashlib.sha1(msg.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

    return msg, msg_hash


def create_plot(html_table: str) -> None:
    data = pd.read_html(html_table, skiprows=1)[0]
    data = data.drop([2], axis=1)
    data.columns = ['Tag', 'Datum', 'Max Temp', 'Min Temp', 'NS']
    data.drop(data.tail(1).index, inplace=True)

    data['date'] = data['Datum'] + ' ' + data['Tag']

    data['Max Temp'] = data['Max Temp'].apply(lambda x: int(x.split('°')[0]))
    data['Min Temp'] = data['Min Temp'].apply(lambda x: int(x.split('°')[0]))
    data['NS'] = data['NS'].apply(lambda x: int(x.split(' ')[0]))

    fig = make_subplots(specs=[[{'secondary_y': True}]])

    fig.add_trace(
        go.Bar(
            x=data['date'],
            y=data['NS'],
            name='Niederschlag',
            marker_color='rgba(0,102,204,0.2)',
            text=data['NS'],
            textposition='auto',
            textfont=dict(color='white'),
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            mode='lines+markers+text',
            x=data['date'],
            y=data['Max Temp'],
            name='Max Temperatur',
            line=dict(color='red'),
            text=data['Max Temp'],
            textposition='bottom center',
            textfont=dict(color='red'),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            mode='lines+markers+text',
            x=data['date'],
            y=data['Min Temp'],
            name='Min Temperatur',
            line=dict(color='orange'),
            text=data['Min Temp'],
            textposition='top center',
            textfont=dict(color='orange'),
        ),
        secondary_y=False,
    )

    fig.update_layout(title_text='Wetteraussichten')

    # Set x-axis title
    fig.update_xaxes(title_text='Datum')

    # Set y-axes titles
    fig.update_yaxes(title_text='Temperatur in [°C]</b> ', secondary_y=False)
    fig.update_yaxes(title_text='Niederschlag in [mm]</b> ', secondary_y=True)

    fig.write_image('overview.png')


def fetch_data():
    fetch_overview()
    fetch_mail_data()


fetch_data()
