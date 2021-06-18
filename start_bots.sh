#!/bin/bash
ps axf | grep /home/samuel/telegram_bots/.venv/bin/python | grep -v grep | awk '{print "kill -9 " $1}' | sh
nohup poetry run python run_bots.py &
