# 449Project5
Members: 
Allison Atienza,
Yujin Chung,
Brian Edwards

Instructions to initialize the databases:

Step 1. Unzip tarball

Step 2. `cd` into directory

Step 3. run `./bin/init.sh`
  
  Note: You should look at the output of this command. It creates 100 users and displays each username and their UUID.
  Save the UUID somewhere so you can easily add a new game record for a user.
  

Instructions to start Traefik:

Step 4. Being in the same directory as from Step 3, run `cd traefik`

Step 5. Install the traefik executable into this folder. We used this version: https://github.com/traefik/traefik/releases/tag/v2.7.0-rc2.

Step 6. Run `./traefik --configFile=traefik.toml`


Instructions to start the service:

Step 7. On ANOTHER TERMINAL, but still in the same directory as in STEP 3, run `foreman start -m api_word=1,api_guess=1,api_stats=3,api_track=1,api_play=1`

Step 8. For each of the 4 services, 
look at `http://localhost:9999/api/word/docs`, `http://localhost:9999/api/guess/docs`, `http://localhost:9999/api/stats/docs`, `http://localhost:9999/api/track/docs`, `http://localhost:9999/api/play/docs`.
(project5 is the Play API)
  
  Note: For /stats/doc, you should see on the command line that the load balancer is working for every refresh or other HTTP method
  

NOTE: All date formats are as followed:

EX: 2021-06-19


Additionally, the words and their word dates go off of the official Wordle game (https://medium.com/@owenyin/here-lies-wordle-2021-2027-full-answer-list-52017ee99e86).

Step 9: Initialize the /bin/crontab file so that it can run its code properly

Step 10: Go to the directory /tmp/materialize.log to see the leaderboards



