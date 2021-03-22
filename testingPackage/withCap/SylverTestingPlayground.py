import math
import random
from myNewBot import myBot
from testingBot import testBot
from testingBot2 import testBot as tBot2
from testingBot3 import testBot as tBot3
from testingBot4 import testBot as tBot4
from numericalSemigroupLite import*

def legalMove(move, movesPlayed, remainingGaps, cap):
    if ((type(move) != int) or move < 1):
        return False
    if (move > cap):
        return False
    if (move in remainingGaps):
        return True
    if((len(remainingGaps) > 0) and (move not in remainingGaps)):
        return False
    if (len(movesPlayed) == 0):
        return True
    S = NumericalSemigroup(movesPlayed)
    return (move not in S)

#PLAYING THE GAME:
def SylverCoinageGame(Player1, Player2, cap = 200, numberOfGames = 100, startingPosition = []):
    p1_wins = 0
    p2_wins = 0
    currentGame = 0
    while(currentGame < numberOfGames):
        remainingGaps = []
        print ("Game ", (currentGame + 1))
        p1_penalties = 0
        p2_penalties = 0
        movesPlayed = [i for i in startingPosition]
        turn = (-1)**((currentGame + 1)+(len(movesPlayed)))
        while(1 not in movesPlayed):
            if(turn == -1):
                move = Player1(movesPlayed, remainingGaps, cap)
            else:
                move = Player2(movesPlayed, remainingGaps, cap)
            if legalMove(move, movesPlayed, remainingGaps, cap):
                movesPlayed.append(move)
                if (gcd_list(movesPlayed) != 1):
                    turn = turn * (-1)
                else:
                    if (len(remainingGaps) == 0):
                        S1 = NumericalSemigroup(movesPlayed)
                        remainingGaps = S1.gaps
                    else:
                        current_linear_combos = [i for i in range(0, max(remainingGaps)) if (i not in remainingGaps)]
                        newGaps = []
                        for i in remainingGaps:
                            i_stays = True
                            for j in current_linear_combos:
                                if((i - j) >= 0) and ((i-j)%move == 0):
                                    i_stays = False
                                    break
                                else:
                                    continue
                            if (i_stays):
                                newGaps.append(i)
                        remainingGaps = [i for i in newGaps]
                    turn = turn * (-1)
            else:
                if(turn == -1):
                    p1_penalties += 1
                    if(p1_penalties >= 3):
                        print("Too many penalties, you lose")
                        movesPlayed.append(1)
                        turn = turn*(-1)
                        p1_penalities = 0
                        p2_penalities = 0
                    else:
                        print("That was not a legal move")
                        continue
                else:
                    p2_penalties += 1
                    if(p2_penalties >= 3):
                        print("Too many penalties, you lose")
                        movesPlayed.append(1)
                        turn = turn*(-1)
                        p1_penalities = 0
                        p2_penalities = 0
                    else:
                        print("That was not a legal move")
                        continue
        if (turn == -1):
            p1_wins += 1
            print (movesPlayed, "Player 1 wins", "Current Score: ", [p1_wins, p2_wins])
        else:
            p2_wins += 1
            print (movesPlayed, "Player 2 wins", "Current Score: ", [p1_wins, p2_wins])
        currentGame += 1
    print("Final Score: ", [p1_wins, p2_wins])
    input("End.")
    return [p1_wins, p2_wins]
    
if __name__ == '__main__':
    numOfGames = int(input("How many games would you like to test the bot? "))
    eachGameCap = int(input("What is the cap for move value (at least 10)?"))
    if(eachGameCap < 10):
        eachGameCap = 10
    SylverCoinageGame(testBot().nextMove, myBot().nextMove, eachGameCap, numOfGames)
