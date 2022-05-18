from re import S
from fastapi import FastAPI, Depends, Response, HTTPException, status
import sqlite3
import contextlib
from datetime import datetime
import httpx
from uuid import UUID
from pydantic import UUID4, BaseModel
import datetime

class Guess(BaseModel):
    user_id: UUID
    guess_word: str
    guess_date: str


class UserGame(BaseModel):
    user_id: UUID
    user_name: str
    game_date: str
    game_id: int

play = FastAPI()

# We are assuming the front end will send the user id AND the username (username is irrelvant in backend procedure though, id matters)
# The code is structured to be that way
# We are also assuming the user chooses what game date to play (which includes game id)
@play.post("/game/new", status_code=status.HTTP_201_CREATED)
async def one_guess(userGame: UserGame):
    new_game = httpx.post('http://localhost:9999/api/track/new_game', 
    json={'user_id':str(userGame.user_id), 'game_id':userGame.game_id})
    if new_game.status_code != httpx.codes.CREATED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Word not found in dictionary."
        )
    return {"status":"new","user_id":userGame.user_id, "game_id":userGame.game_id}


# We are assuming the client sends the game id's corresponding date to the backend
# guess date is the true id because the code is structured to have one word correspond to one day
@play.post("/game/{game_id}", status_code=status.HTTP_201_CREATED)
async def one_guess(guess: Guess, game_id):
    verify_dict = httpx.get('http://localhost:9999/api/word/word', params={'user_word': '{}'.format(guess.guess_word)})
    if verify_dict.status_code != httpx.codes.OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Word not found in dictionary."
        )
    check_guess = httpx.post('http://localhost:9999/api/track/restore_game', params={'user_id':guess.user_id})
    if check_guess.status_code != httpx.codes.OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist or user is not playing any games currently."
        )
    if not check_guess.json()['guesses_left'] > 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No more guesses."
        )
    print(check_guess.json()['guesses_left'])
    
    
    
    
    analyze_guess = httpx.get('http://localhost:9999/api/guess/guess', params={'guess_date': '{}'.format(guess.guess_date), 'input':'{}'.format(guess.guess_word)})
    if analyze_guess.status_code != httpx.codes.OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid date"
        )
    update_game = httpx.post('http://localhost:9999/api/track/update_game', params={'user_id':guess.user_id, 'input_word':guess.guess_word})
    if update_game.status_code != httpx.codes.OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No more guesses!"
        )
    if analyze_guess.json()['analysis']==['green']*5:
        add_win = httpx.post('http://localhost:9999/api/stats/stats', json={'user_id':str(guess.user_id), 'game_id':game_id, 'timestamp':str(datetime.datetime.now()),
    	'guesses':6-check_guess.json()['guesses_left']+1,'won':True})
        if add_win.status_code != httpx.codes.CREATED:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
            )
        get_stats = httpx.get('http://localhost:9999/api/stats/stats', params={'user_id': '{}'.format(str(guess.user_id))})
        return {"user_id": guess.user_id, "stats":get_stats.json(), "analysis":analyze_guess.json()['analysis']}
        
    else:
        if check_guess.json()['guesses_left']-1 == 0:
            add_lose = httpx.post('http://localhost:9999/api/stats/stats', json={'user_id':str(guess.user_id), 'game_id':game_id, 'timestamp':str(datetime.datetime.now()),
    	'guesses':6-check_guess.json()['guesses_left']+1,'won':False})
            if add_lose.status_code != httpx.codes.CREATED:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
                )
            get_stats = httpx.get('http://localhost:9999/api/stats/stats', params={'user_id': '{}'.format(str(guess.user_id))})
            print("FAIL")
            return {"user_id": guess.user_id, "stats":get_stats.json(), "analysis":analyze_guess.json()['analysis']}
        else:
            return {"user_id": guess.user_id, "guess_date":guess.guess_date, "game_id":game_id, "analysis":analyze_guess.json()['analysis']}
