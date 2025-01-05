Developed a scrabble bot as part of a team which works in the dedicated enviornment provided by our professor. 


--The file scrabble_ai is where our bot lives (this is the only piece of code we developed directly)-- 

* board.py: Board information such as displaying the board, what letters each person has, ...
* gatekeeper.py: An intermediary allowing our bot to access some information about the board without giving us full authority
* incrementalist.py: A very simple and weak example scrabble bot provided by our professor. The only example given. 
* location.py: Contains information on how to place tiles
* move.py: Contains functions for us to play a move
* tournament.py: Can conduct a round robin tournament of numerous bots and scores up the winners and losers
* words.txt: a list of all valid scrabble words


* scrabble_gui.py: Where we can actually play against a bot or put two bots against each other, has a visual display 
* scrabble_ai.py: Our scrabble bot (NigelRichards), the place we developed all the code for. Works by scanning the board to see what tiles are available and uses seperate functions to test letters given in our hand alongside letters on the board to find the best scoring possibility. Has some foresights as we had limited time to implement this; doesn't play words across multiple letters or find words attached to the sides of letters, doesn't utilize any advanced predictive capabilities in scrabble such as blocking. Still a strong bot which only an expierenced scrabbler could beat.   


