import math
import random
from numericalSemigroupLite import*
from myNewBot import myBot
from testingBot import testBot

def legalMove(move, movesPlayed, remainingGaps):
    if ((type(move) != int) or move < 1):
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
def SylverCoinageGame(Player1, Player2, numberOfGames = 100, startingPosition = []):
    p1_wins = 0
    p2_wins = 0
    currentGame = 0
    while(currentGame < numberOfGames):
        remainingGaps = []
        print ("Game ", (currentGame + 1))
        p1_penalties = 0
        p2_penalties = 0
        if(0 in startingPosition):
            remainingGaps = startingPosition[1:]
            movesPlayed = []
        else:
            movesPlayed = [i for i in startingPosition]
        turn = (-1)**((currentGame + 1)+(len(movesPlayed)))
        while(1 not in movesPlayed):
            if(turn == -1):
                move = Player1(movesPlayed, remainingGaps)
            else:
                move = Player2(movesPlayed, remainingGaps)
            if legalMove(move, movesPlayed, remainingGaps):
                movesPlayed.append(move)
                if ((gcd_list(movesPlayed) != 1) and (len(remainingGaps) == 0)):
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

def setCap(n):
    return [i for i in range(0, n+1)]

def checkForCap():
    check = input('Would you like to cap the games? (y/n) ')
    if(check == 'y'):
        return True
    elif(check == 'n'):
        return False
    else:
        return checkForCap()
    
    
if __name__ == '__main__':
    numOfGames = int(input("How many games would you like to test the bot? "))
    if(checkForCap()):
        cap = int(input("Cap value: "))
        SylverCoinageGame(testBot().nextMove, myBot().nextMove, numOfGames, setCap(cap))
    else:
        SylverCoinageGame(testBot().nextMove, myBot().nextMove, numOfGames)
    
