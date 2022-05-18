#!/bin/sh

sqlite3 ./database/wordle.db < ./bin/wordle_init.sql
sqlite3 ./database/dict.db < ./bin/dict_init.sql
python3 ./bin/stats_init.py
python3 ./bin/wordle_pop.py
python3 ./bin/dict_pop.py

