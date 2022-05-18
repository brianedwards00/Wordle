from re import S
from fastapi import FastAPI, Depends, Response, HTTPException, status
import sqlite3
import contextlib
from datetime import datetime



validate = FastAPI()
   
# Input: user word
# Output: JSON representation on whether the word is a valid dictionary word or not
@validate.get("/word", status_code=status.HTTP_200_OK)
async def validate_word(user_word: str, response: Response):
    con = sqlite3.connect('./database/dict.db')
    cursor = con.cursor()
    try:
        dict_word = cursor.execute("SELECT word FROM dict WHERE word = ?", [user_word.lower()]).fetchone()[0]
        con.close()
        return {"guess": "valid", "user_word": user_word.lower()}
    except:
        con.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid word"
        )


# Input: user word
# Output: JSON representation on whether the word was added to the database or not
@validate.post("/word", status_code=status.HTTP_201_CREATED)
async def add_word(user_word: str, response: Response):
    if len(user_word) > 5:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Input not 5 characters"
        )
    con = sqlite3.connect('./database/dict.db')
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO dict(word) VALUES(?)",[user_word.lower()])
        con.commit()
        con.close()
    except sqlite3.IntegrityError as e:
        con.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    response.headers["Location"] = f"/word?user_word={user_word.lower()}"
    return {"user_word": user_word.lower(), "db_id": cursor.lastrowid}


# Input: user word
# Output: JSON representation on whether the word was added to the database or not
@validate.delete("/word", status_code=status.HTTP_200_OK)
async def delete_word(user_word: str, response: Response):
    if len(user_word) > 5:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Input not 5 characters"
        )
    con = sqlite3.connect('./database/dict.db')
    cursor = con.cursor()
    try:
        cursor.execute("SELECT word FROM dict WHERE word = ?", [user_word.lower()]).fetchone()[0]
        cursor.execute("DELETE FROM dict WHERE word = ?", [user_word.lower()])
        con.commit()
        con.close()
    except:
        con.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Word Not Found"
        )
    response.headers["Deleted"] = f"/word?user_word={user_word.lower()}"
    return {"deleted": user_word.lower()}

