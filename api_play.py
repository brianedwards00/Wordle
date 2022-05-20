from re import S
from fastapi import FastAPI, Depends, Response, HTTPException, status
import sqlite3
import contextlib
from datetime import datetime
import httpx
from uuid import UUID
from pydantic import UUID4, BaseModel
import datetime
import random


won = False

class Guess(BaseModel):
    user_id: UUID
    guess_word: str
    


class UserGame(BaseModel):
    user_id: UUID
    user_name: str

play = FastAPI()

# We are assuming the front end will send the user id AND the username (username is irrelvant in backend procedure though, id matters)
# The code is structured to be that way
@play.post("/game/new", status_code=status.HTTP_201_CREATED)
async def one_guess(userGame: UserGame):
    check_guess = httpx.post('http://localhost:9999/api/track/restore_game', params={'user_id':userGame.user_id})
    if check_guess.status_code == httpx.codes.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No Content."
        )
    elif check_guess.status_code == httpx.codes.OK and int(check_guess.json()['guesses_left'])!=0:
        return {"status":"in-progress","user_id":userGame.user_id, "game_id": int(check_guess.json()['current_game_id']), "remaining":check_guess.json()['guesses_left'], "guesses":check_guess.json()['guesses']} 
    check = False
    game_id=0
    while not check:
        game_id = random.randint(0,2300)
        new_game = httpx.post('http://localhost:9999/api/track/new_game', 
            json={'user_id':str(userGame.user_id), 'game_id':game_id})
        if new_game.status_code == httpx.codes.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not playing a game."
            )
        elif new_game.status_code == httpx.codes.BAD_REQUEST:
            print("You already played this. Trying another id....")
        else:
            check = True
    return {"status":"new","user_id":userGame.user_id, "game_id":game_id}


# We are assuming the client sends the correct game id because it was provided in /game/new
@play.post("/game/{game_id}", status_code=status.HTTP_201_CREATED)
async def one_guess(guess: Guess, game_id, response: Response):
    check_guess = httpx.post('http://localhost:9999/api/track/restore_game', params={'user_id':guess.user_id})
    if check_guess.status_code != httpx.codes.OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist or user is not playing any games currently."
        )
    verify_dict = httpx.get('http://localhost:9999/api/word/word', params={'user_word': '{}'.format(guess.guess_word)})
    if verify_dict.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "invalid", "remaining":check_guess.json()['guesses_left']}
    if not check_guess.json()['guesses_left'] > 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No Content."
        )
    print(check_guess.json()['guesses_left'])
    
    
    
    
    analyze_guess = httpx.get('http://localhost:9999/api/guess/guess', params={'guess_id': '{}'.format(game_id), 'input':'{}'.format(guess.guess_word)})
    print(analyze_guess.json()['analysis'])
    if analyze_guess.status_code != httpx.codes.OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid id. Please start a new game."
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
        for i in range(0,5):
            update_game = httpx.post('http://localhost:9999/api/track/update_game', params={'user_id':guess.user_id, 'input_word':guess.guess_word})
        return {"user_id": guess.user_id,"status":"win", "stats":get_stats.json(), "analysis":analyze_guess.json()['analysis']}
        
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
            print(get_stats.json())
            return {"user_id": guess.user_id, "stats":get_stats.json(), "analysis":analyze_guess.json()['analysis']}
        else:
            return {"status": "incorrect", "remaining":check_guess.json()['guesses_left']-1, "analysis":analyze_guess.json()['analysis']}
