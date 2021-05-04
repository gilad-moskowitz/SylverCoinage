import random
from numericalSemigroupLite import *
from testingBot4 import testBot as randomBot
from oldUpdatedBestBot import myBot as oldBestBot

class democrat:
    def __init__(self):
        pass
    
    def coverRelations(self, gap):
        if(len(gap) == 0):
            return {}
        linComb = [i for i in range(0, max(gap) + 1) if i not in gap]
        dictionary = {};
        for i in range(0, len(gap)):
            covers = []
            for j in range(i + 1, len(gap)):
                for k in range(0, len(linComb)):
                    if(gap[j] - linComb[k] < gap[i]):
                        break
                    if(((gap[j] - linComb[k]) > 0) and ((gap[j] - linComb[k])%gap[i] == 0)):
                        covers.append(gap[j])
                        break
            dictionary[gap[i]] = covers
        return dictionary
    
    def pretendMove(self, gaps, pretend):
        covering = self.coverRelations(gaps)
        return [i for i in gaps if((i not in covering[pretend]) and (i != pretend))]
    
    def democracyAlgorithm(self, movesPlayed, gaps, gamesToPlay = 1000):
        probs = {}
        badMoves = []
        for move in gaps:
            if(move == 1):
                continue
            testing = self.pretendMove(gaps, move)
            count = 0
            Wins = 0
            Loses = 0
            bestResponse = []
            rebuttal = []
            winsInARow = 0
            lossesInARow = 0
            for currentRun in range(0, gamesToPlay):
                moves = [i for i in movesPlayed]
                moves.append(move)
                temp = [i for i in testing]
                initialRebuttal = []
                initialResponse = []
                while(temp != [1]):
                    if((count == 0) and (len(bestResponse) > 0)):
                        newMove = bestResponse[0]
                        moves.append(newMove)
                        count += 1
                        temp = self.pretendMove(temp, newMove)
                        continue
                    if((count == 1) and (len(bestResponse) > 0) and (len(rebuttal) > 0)):
                        newMove = rebuttal[0]
                        moves.append(newMove)
                        count += 1
                        temp = self.pretendMove(temp, newMove)
                        continue
                    moveChoices = [i for i in temp if(i != 1)]
                    if(count%2 == 0):
                        newMove = randomBot().nextMove(moves, temp)
                    else:
                        newMove = oldBestBot().nextMove(moves, temp)
                    if(count == 0):
                        initialResponse.append(newMove)
                    if(count == 1):
                        initialRebuttal.append(newMove)
                    moves.append(newMove)
                    count += 1
                    temp = self.pretendMove(temp, newMove)
                if(count%2 == 0):
                    if((len(bestResponse) != 0) and (len(rebuttal) == 0)):
                        rebuttal.append(initialRebuttal[0])
                    if(lossesInARow == 0):
                        rebuttal = []
                        winsInARow += 1
                    else:
                        rebuttal = []
                        lossesInARow = 0
                        winsInARow += 1
                    if(winsInARow >= 0.08*gamesToPlay):
                        Wins = gamesToPlay - Loses
                        break
                    Wins += 1
                else:
                    if(len(bestResponse) == 0):
                        bestResponse.append(initialResponse[0])
                    if(winsInARow == 0):
                        bestResponse = []
                        lossesInARow += 1
                    else:
                        winsInARow = 0
                        lossesInARow += 1
                    if(lossesInARow >= 0.08*gamesToPlay):
                        badMoves.append(move)
                        break
                    Loses += 1
                count = 0
            probs[move] = Wins/gamesToPlay
        bestMove = 1
        bestProb = 0
        for pot in probs:
            if(probs[pot] > bestProb):
                bestProb = float(probs[pot])
                bestMove = int(pot)
        if(bestMove == 1):
            return(max(gaps))
        return bestMove
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        movesPlayed = [int(i) for i in movesPlayed]
        remainingMoves = [i for i in remainingGaps]
        if((len(remainingMoves) < 50) and (len(remainingMoves) > 0) and (len(movesPlayed) != 0)):
            return self.democracyAlgorithm(movesPlayed, remainingMoves, int(1000/len(remainingMoves)))
        #NORMAL STUFF
        elif((len(remainingMoves)>0) and (len(movesPlayed) != 0)):
            if((len(remainingMoves)%2) == 0):
                return max(remainingMoves)
            else:
                linearCombos = [i for i in range(1, max(remainingMoves)) if i not in remainingMoves]
                j = len(remainingMoves) - 1
                while(j > 2):
                    for l in linearCombos:
                        if (((remainingMoves[j] - l) in remainingMoves) and ((remainingMoves[j] - l) > 3)):
                            return (remainingMoves[j] - l)
                        else:
                            continue
                    j -= 1
                return max(remainingMoves)
        elif(len(movesPlayed) == 0):
            return random.choice([5, 7, 11, 13, 17, 19, 23, 29])
        elif(len(movesPlayed) == 1):
            factors = PrimeFactorization(movesPlayed[0])
            if (len(factors) == 1):
                possible = [i for i in range(movesPlayed[0] + 1, max(100, movesPlayed[0] + 1)) if((i%movesPlayed[0]) != 0)]
                index = random.randint(0, len(possible) - 1)
                return possible[index]
            elif(max(factors) > 3):
                return max(factors)
            else:
                newMove = 1
                for a in factors:
                    newMove = newMove*a
                return int(((newMove/min(factors)) + 1)*min(factors))
        else:
            gcd_moves = gcd_list(movesPlayed)
            newSet = [int(i/gcd_moves) for i in movesPlayed]
            if ((1 in newSet) and (gcd_moves > 1)):
                return (gcd_moves*2 + 1)
            S = NumericalSemigroup(newSet)
            remainingMoves = S.gaps
            if((len(remainingMoves) <= 1) and gcd_moves > 1):
                return (gcd_moves*2 + 1)
            else:
                if((len(remainingMoves)%2) == 0):
                    return (max(remainingMoves)*gcd_moves)
                else:
                    linearCombos = [i for i in range(1, max(remainingMoves)) if i not in remainingMoves]
                    j = len(remainingMoves) - 1
                    while(j > 2):
                        for l in linearCombos:
                            if (((remainingMoves[j] - l) in remainingMoves) and ((remainingMoves[j] - l) > 3)):
                                return ((remainingMoves[j] - l)*gcd_moves)
                            else:
                                continue
                        j -= 1
                    return (max(remainingMoves)*gcd_moves)