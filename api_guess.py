from re import S
from fastapi import FastAPI, Depends, Response, HTTPException, status
import sqlite3
import contextlib
from datetime import datetime


check = FastAPI()

@check.get("/guess", status_code=status.HTTP_200_OK)
async def analyze_guess(guess_id: int, input: str):
    guess_word = input.lower()
    con = sqlite3.connect('./database/wordle.db', check_same_thread=False)
    cursor = con.cursor()
    try:
        actual_word = cursor.execute("SELECT answer FROM wordle WHERE id = ?", [guess_id]).fetchone()[0]
        con.close()
    except:
        con.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid id"
        )
    print(actual_word)
    actual_counter = 0
    pre_analysis = ["red"] * 5
    for actual_l in actual_word:
        guess_counter = 0
        for guess_l in guess_word:
            if guess_counter == actual_counter and actual_l == guess_l:
                pre_analysis[guess_counter] = "green"
            elif actual_l == guess_l:
                pre_analysis[guess_counter] = "yellow"
            guess_counter += 1
        actual_counter += 1
    analysis = pre_analysis
    if sum(1 for i in analysis if i == "yellow") == 1 and sum(1 for i in analysis if i == "green"):
        analysis = ["green"] * 5
    return {"guess_id": guess_id, "input": input.lower(), "analysis": analysis}
