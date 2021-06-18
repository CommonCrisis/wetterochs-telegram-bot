# Telegram bot for the so called Wetter Ochs
https://www.wettermail.de/

## Dependencies
 - poetry (https://python-poetry.org/)
 - npm (https://www.npmjs.com/) or conda (https://docs.conda.io/en/latest/)
 - orca (https://github.com/plotly/orca)
 - .env with a Telegram bot token
 ```
 WO_BOT_TOKEN=<my long telegram bot token>
 ```


## Run
```bash
bash start_bots.sh
```
to run the bot as background process
```bash
poetry run python run_bots.py
```
to run the bot in python
