# SylverCoinage
This contains the code (SageMath) used for testing and running Sylver Coinage games. 

You must have the NumericalGapsPackage installed in the same place as the files from this repository. 

Sylver Coinage:
GAMEPLAY:
Sylver Coinage is a game played between two players. On each player’s turns they list a positive integer that can’t be made as a linear combination of the previously named numbers. The first player to pick the number 1, loses. An example game could work as follows:
Player 1 picks the number 4
	Now no player can pick any multiple of 4
Player 2 picks the number 5
	The only numbers left that players can now pick are: {1, 2, 3, 6, 7, 11}
	9 for instance can be made using one 4 and one 5. 
To show that any number greater than 4 also can be made using 4’s and 5’s we see the following:
	12 can be made by three 4’s
	13 can be made with two 4’s and a 5
	14 can be made with two 5’s and a 4
	15 can be made with three 5’s
	Now every number can be made as 12 + 4k, 13 + 4k, 14 + 4k, or 15 + 4k for k >= 0
Player 1 picks 11
	The only numbers left that players can pick from are: {1, 2, 3, 6, 7}
Player 2 picks 7
	The only numbers left that players can pick from are: {1, 2, 3, 6}
Player 1 picks 6
	The only numbers left that players can pick from are: {1, 2, 3}
Player 2 picks 3
	The only numbers left that players can pick from are: {1, 2}
Player 1 picks 2
	The only number left that players can pick from are: {1}
So player 2 must choose 1 and therefore lose. 


THE GOAL:
Design a bot that plays the game best under all circumstances. This means that whatever the starting move, the bot still makes the best move from there. There are known states that result in winning and losing positions, but there are only complete strategies for a very small number of starting states. 
RULES FOR THE BOT:
•	The program that tests the bots is written in SageMath (python 2) and each “player” is a function that gets called. 
•	The inputs for the function are 1) The moves played so far, 2) The remaining possible moves if there is a finite number of them
•	The function returns an integer which represents its move
•	If the function returns an integer that is not a legal move, they earn a penalty. If, during a single game a player gets 3 penalties, they are forced to choose 1 and they lose the game. 
RULES FOR THE TOURNAMENT:
•	The tournament will be a round robin tournament wherein each bot plays matches with each other both 3 times.
•	Each match consists of 100 games and the match is scored based on the number of games the bot won more than 50 in a match. The exact scoring system is still being worked on.
•	The bot with the best score at the end of the tournament will win a free dinner for their creator.  
