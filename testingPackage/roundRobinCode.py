from fullSemigroupPackage import*


def legalMove(move, movesPlayed, remainingGaps = []):
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

def SylverCoinageGame(Player1, Player2, numberOfGames = 100, startingPosition = []):
    p1_wins = 0
    p2_wins = 0
    currentGame = 0
    lossByPenalties = False
    while(currentGame < numberOfGames):
        remainingGaps = []
        print ("Game ", (currentGame + 1))
        p1_penalties = 0
        p2_penalties = 0
        movesPlayed = [i for i in startingPosition]
        turn = (-1)**((currentGame + 1)+(len(movesPlayed)))
        while(1 not in movesPlayed):
            if(turn == -1):
                move = Player1(movesPlayed, remainingGaps)
            else:
                move = Player2(movesPlayed, remainingGaps)
            if legalMove(move, movesPlayed, remainingGaps):
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
                        p1_penalities = 0
                        p2_penalities = 0
                        lossByPenalties = True
                    else:
                        print("That was not a legal move")
                        continue
                else:
                    p2_penalties += 1
                    if(p2_penalties >= 3):
                        print("Too many penalties, you lose")
                        movesPlayed.append(1)
                        p1_penalities = 0
                        p2_penalities = 0
                        lossByPenalties = True
                    else:
                        print("That was not a legal move")
                        continue
        if(lossByPenalties):
            turn = turn*(-1)
            lossByPenalties = False
        if (turn == -1):
            p1_wins += 1
            print (movesPlayed, "Player 1 wins", "Current Score: ", [p1_wins, p2_wins])
        else:
            p2_wins += 1
            print (movesPlayed, "Player 2 wins", "Current Score: ", [p1_wins, p2_wins])
        currentGame += 1
    print("Final Score: ", [p1_wins, p2_wins])
    return [p1_wins, p2_wins]

def roundRobinTourney(listOfBots, numberOfRounds = 3, gamesPerMatch = 100, startingPosition = []): 
    bestBot = {}
    for i in range(1, len(listOfBots) + 1):
        bestBot[i] = [0, 0, 0, 0]
    currentRound = 1
    while(currentRound <= numberOfRounds):
        j = 0
        k = 1
        while(j < len(listOfBots)):
            while(k < len(listOfBots)):
                A = SylverCoinageGame(listOfBots[j], listOfBots[k], gamesPerMatch, startingPosition)
                if(A[0] > A[1]):
                    bestBot[j + 1][0] += 3
                elif(A[0] < A[1]):
                    bestBot[k + 1][0] += 3
                else:
                    bestBot[j + 1][0] += 1
                    bestBot[k + 1][0] += 1
                bestBot[j + 1][1] += A[0]
                bestBot[k + 1][1] += A[1]
                bestBot[j + 1][2] += A[0] - A[1]
                bestBot[k + 1][2] += A[1] - A[0]
                bestBot[j + 1][3] += A[0] - 50
                bestBot[k + 1][3] += A[1] - 50
                k += 1
            j += 1
            k = (j + 1)
        currentRound += 1
    return bestBot