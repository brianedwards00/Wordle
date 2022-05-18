import os
import os.path
import sqlite3
from fastapi import FastAPI, Depends, Response, HTTPException, status
from uuid import UUID
import redis

topWins = {}
for i in range(1,4):
    con = sqlite3.connect(f'/home/student/Desktop/4project/database/games{i}.db')
    cursor = con.cursor()
    try:
        top_wins = cursor.execute("SELECT user_id, `COUNT(won)` FROM wins "
            "ORDER BY `COUNT(won)` DESC LIMIT 10").fetchall()
        con.close()
        for win in top_wins:
            topWins.update({UUID(bytes_le=win[0]): win[1]})
    except:
        con.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error"
            )

topWins_ordered = {user_id: win_count for user_id, win_count in sorted(topWins.items(), key=lambda query: query[1], reverse=True)}
topWins_keys = list(topWins_ordered)
r = redis.Redis()
top_wins = "top_wins"
r.delete("top_wins")
for i in range(0, len(topWins_keys)):
    key = topWins_keys[i].bytes_le
    value = topWins_ordered[topWins_keys[i]]
    r.zadd(top_wins, {key: value})
    
    

topStreaks = {}
# In each database, collect the top 10 streaks for a total of 30 k/v values in topStreaks
for i in range(1,4):
    con = sqlite3.connect(f'/home/student/Desktop/4project/database/games{i}.db')
    cursor = con.cursor()
    try:
        top_streaks = cursor.execute("SELECT user_id, streak FROM streaks "
        "ORDER BY streak DESC LIMIT 10").fetchall()
        con.close()
        for streak in top_streaks:
            topStreaks.update({UUID(bytes_le=streak[0]): streak[1]})
    except:
        con.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error"
        )
# Order topStreaks based on streak count
topStreaks_ordered = {user_id: streak_count for user_id, streak_count in sorted(topStreaks.items(), key=lambda query: query[1], reverse=True)}
topStreaks_keys = list(topStreaks_ordered)
top_streaks = "top_streaks"
r.delete("top_streaks")
for i in range(0, len(topStreaks_keys)):
    key = topStreaks_keys[i].bytes_le
    value = topStreaks_ordered[topStreaks_keys[i]]
    r.zadd(top_streaks, {key: value})

print("TOP WINS")
print(r.zrange(top_wins, 0, -1, withscores=True))
print("TOP STREAKS")
print(r.zrange(top_streaks, 0, -1, withscores=True))
print('\n\n')
