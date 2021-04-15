import time
import pandas as pd
try:
    from numericalSemigroupLite import*
except:
    raise Exception("No access/couldn't find to numericalSemigroupLite.py'") from None
try:
    from bestBot import myBot as bestBot
except:
    print("WARNING! No access/couldn't find to bestBot.py'")
try:
    from mediumBot import myBot as mediumBot
except:
    print("WARNING! No access/couldn't find to mediumBot.py'")
try:
    from betterBot import myBot as betterBot
except:
    print("WARNING! No access/couldn't find to betterBot.py'")
try:
    from worstBot import testBot as worstBot
except:
    print("WARNING! No access/couldn't find to worstBot.py'")
try:
    from randomBot import testBot as randomBot
except:
    print("WARNING! No access/couldn't find to randomBot.py'")
#ADDING YOUR OWN BOT CODE
try:
    from myOwnBot import myBot
except:
    print("WARNING! No access/couldn't find to myOwnBot.py'")



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
    p1_totalTime = 0
    p1_totalMoves = 0
    p2_totalTime = 0
    p2_totalMoves = 0
    currentGame = 0
    lossByPenalties = False
    while(currentGame < numberOfGames):
        remainingGaps = []
        print ("Game ", (currentGame + 1))
        p1_penalties = 0
        p2_penalties = 0
        p1_time = 0
        p2_time = 0
        p1_moves = 0
        p2_moves = 0
        gameManagementTotalTime = 0
        movesPlayed = [i for i in startingPosition]
        turn = (-1)**((currentGame + 1)+(len(movesPlayed)))
        while(1 not in movesPlayed):
            if(turn == -1):
                start = time.perf_counter()
                move = Player1(movesPlayed, remainingGaps)
                p1_time += time.perf_counter() - start
                p1_moves += 1
            else:
                start = time.perf_counter()
                move = Player2(movesPlayed, remainingGaps)
                p2_time += time.perf_counter() - start
                p2_moves += 1
            gameStart = time.perf_counter()
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
            gameManagementTotalTime += time.perf_counter() - gameStart
        if(lossByPenalties):
            turn = turn*(-1)
            lossByPenalties = False
        if (turn == -1):
            p1_wins += 1
            print (movesPlayed, "Player 1 wins", "Current Score: ", [p1_wins, p2_wins])
        else:
            p2_wins += 1
            print (movesPlayed, "Player 2 wins", "Current Score: ", [p1_wins, p2_wins])
        print("Player 1, total moves: ", p1_moves, " total time (s): ", p1_time, " average time (s) per move: ", (p1_time/p1_moves))
        print("Player 2, total moves: ", p2_moves, " total time (s): ", p2_time, " average time (s) per move: ", (p2_time/p2_moves))
        print("Game management time (s): ", gameManagementTotalTime)
        p1_totalTime += p1_time
        p2_totalTime += p2_time
        p1_totalMoves += p1_moves
        p2_totalMoves += p2_moves
        currentGame += 1
    print("Final Score: ", [p1_wins, p2_wins])
    return [p1_wins, p2_wins], [p1_totalMoves, p1_totalTime, (p1_totalTime/p1_totalMoves)], [p2_totalMoves, p2_totalTime, (p2_totalTime/p2_totalMoves)]

def roundRobinTourney(listOfBots, numberOfRounds = 3, gamesPerMatch = 100, startingPosition = []): 
    bestBot = {}
    for i in range(1, len(listOfBots) + 1):
        bestBot[i] = [0, 0, 0, 0, 0, 0, 0]
    currentRound = 1
    while(currentRound <= numberOfRounds):
        j = 0
        k = 1
        while(j < len(listOfBots)):
            while(k < len(listOfBots)):
                A = SylverCoinageGame(listOfBots[j], listOfBots[k], gamesPerMatch, startingPosition)
                if(A[0][0] > A[0][1]):
                    bestBot[j + 1][0] += 3
                elif(A[0][0] < A[0][1]):
                    bestBot[k + 1][0] += 3
                else:
                    bestBot[j + 1][0] += 1
                    bestBot[k + 1][0] += 1
                bestBot[j + 1][1] += A[0][0]
                bestBot[k + 1][1] += A[0][1]
                bestBot[j + 1][2] += A[0][0] - A[0][1]
                bestBot[k + 1][2] += A[0][1] - A[0][0]
                bestBot[j + 1][3] += A[0][0] - (gamesPerMatch/2)
                bestBot[k + 1][3] += A[0][1] - (gamesPerMatch/2)
                bestBot[j + 1][4] += A[1][0]
                bestBot[j + 1][5] += A[1][1]
                bestBot[j + 1][6] += A[1][2]
                bestBot[k + 1][4] += A[2][0]
                bestBot[k + 1][5] += A[2][1]
                bestBot[k + 1][6] += A[2][2]
                k += 1
            j += 1
            k = (j + 1)
        currentRound += 1
    for a in bestBot:
        bestBot[a][6] = bestBot[a][6]/numberOfRounds
    df = pd.DataFrame.from_dict(bestBot, orient='index', columns=['Match Score', 'Total Wins','Total Wins - Total Losses', 'Wins above 50%', 'Total Moves', 'Total Time', 'Average Time Per Move'])
    return df
    
if __name__ == '__main__':
    allBots = []
    allBotNames = ["bestBot", "oldBestBot", "mediumOldBot", "betterOldBot", "worstBot", "randomBot", "myBot"]
    try:
        allBots.append(bestBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("bestBot"))
    try:
        allBots.append(oldBestBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("oldBestBot"))
    try:
        allBots.append(mediumOldBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("mediumOldBot"))
    try:
        allBots.append(betterOldBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("betterOldBot"))
    try:
        allBots.append(worstBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("worstBot"))
    try:
        allBots.append(randomBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("randomBot"))
    try:
        allBots.append(myBot().nextMove)
    except:
        allBotNames.pop(allBotNames.index("myBot"))
    
    if(len(allBots) == 0):
        input("Oh no, you don't have access to any bots. Please download the necessary files and try again.")
    else:
        print("You have access to the following bots using the corresponding numbers: ")
        for i in range(0, len(allBots)):
            print(i, ": ", allBotNames[i])
        remainingMoves = []
        withCapAnswer = str(input("Would you like to cap the move value that the bots can play? (y/n) "))
        if(withCapAnswer.lower() == "y" or withCapAnswer.lower() == "yes" or withCapAnswer == "1"):
            capValue = int(input("What value (exclusive) would you like the cap? "))
            remainingMoves = [i for i in range(0, capValue)]
        if(len(allBots) > 1):
            roundRobin = False
            answer = str(input("Would you like a round robin tournament with all the bots you have access to? (y/n) "))
            if(answer.lower() == "y" or answer.lower() == "yes" or answer == "1"):
                numOfGames = int(input("How many games would you the bots to play per match? "))
                numOfRound = int(input("How many rounds would you the bots to play? "))
                results = roundRobinTourney(allBots, numOfRound, numOfGames, remainingMoves)
                print(results)
                input("End.")
            else:
                first = int(input("What is the number corresponding the the first bot you would like to test? "))
                second = int(input("What is the number corresponding the the second bot you would like to test? "))
                numOfGames = int(input("How many games would you the bots to play? "))
                SylverCoinageGame(allBots[first], allBots[second], numOfGames, remainingMoves)
                input("End.")
        else:
            first = int(input("What is the number corresponding the the first bot you would like to test? "))
            second = int(input("What is the number corresponding the the second bot you would like to test? "))
            numOfGames = int(input("How many games would you the bots to play? "))
            SylverCoinageGame(allBots[first], allBots[second], numOfGames, remainingMoves)
            input("End.")
