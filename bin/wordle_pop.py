import sqlite3
import json
import os
import os.path
import datetime

if os.path.isfile('answers.json'):
    os.remove('answers.json')

os.system("curl --silent https://www.nytimes.com/games/wordle/main.bfba912f.js |sed -e 's/^.*var Ma=//' -e 's/,Oa=.*$//' -e 1q > answers.json")

#import and load the answers file into a variable
answers_file = open('answers.json')
answers_data = json.load(answers_file)

#create a Connection object that represents the database
con = sqlite3.connect('./database/wordle.db') 

#create a Cursor object and call execute method to perform SQL commands
cur = con.cursor() 

start_date = datetime.date(2021, 6, 19)
delta = datetime.timedelta(days=1)

#populate the database with the JSON answers; insert the answers into rows
for x in range(len(answers_data)):
    cur.execute("INSERT INTO wordle (id, answer,answer_date) values (?, ?, ?)", (x, answers_data[x], start_date))
    start_date += delta

#Save the changes
con.commit()

#Close the connection
con.close()
if os.path.isfile('answers.json'):
    os.remove('answers.json')
