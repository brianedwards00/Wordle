import sqlite3
import json
import os
import os.path
import datetime

if os.path.isfile('words'):
    os.remove('words')

os.system("cp /usr/share/dict/words ./words")

word_file = open("./words", 'r')
valid_words = []
for line in word_file:
    if len(line.rstrip('\n')) == 5 and "'" not in line and line[0].isupper() == False and 'é' not in line:
        word = line.replace('\n','')
        valid_words.append(word)

#create a Connection object that represents the database
con = sqlite3.connect('./database/dict.db') 

#create a Cursor object and call execute method to perform SQL commands
cur = con.cursor()

#populate the database with the JSON answers; insert the answers into rows
for x in range(len(valid_words)):
    cur.execute("INSERT INTO dict (id, word) values (?, ?)", (x, valid_words[x]))

#Save the changes
con.commit()

#Close the connection
con.close()
if os.path.isfile('words'):
    os.remove('words')
