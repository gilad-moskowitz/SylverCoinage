import random
from numericalSemigroupLite import *

class weakCounter:
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
    
    def checkWeaklyLostPosition(self, gaps):
        moveCountermoveDict = {}
        alreadyPaired = []
        isSingle = []
        for a in gaps:
            if(a not in alreadyPaired):
                moveCountermoveDict[a] = []
                nextStage = self.pretendMove(gaps, a)
                covers = self.coverRelations(nextStage)
                for g in nextStage:
                    if((g > 1) and ((len(nextStage) - len(covers[g]))%2 == 0) and (g not in alreadyPaired) and (g not in isSingle)):
                        moveCountermoveDict[a].append(g)
                        moveCountermoveDict[g] = [a]
                        alreadyPaired.append(a)
                        alreadyPaired.append(g)
                        break
                    else:
                        isSingle.append(a)
        isWeaklyLost = True
        for move in moveCountermoveDict:
            if (move > 1):
                if(len(moveCountermoveDict[move]) == 0):
                    isWeaklyLost = False
                    break
        return isWeaklyLost, moveCountermoveDict
    
    def checkWeak(self, gaps):
        moveCountermoveDict = {}
        alreadyPaired = []
        isSingle = []
        for a in gaps:
            if(a > 1):
                moveCountermoveDict[a] = []
                nextStage = self.pretendMove(gaps, a)
                covers = self.coverRelations(nextStage)
                for g in nextStage:
                    if((g > 1) and ((len(nextStage) - len(covers[g]))%2 == 0)):
                        if(a > g):
                            if(a in moveCountermoveDict[g]):
                                moveCountermoveDict[a].append(g)
                                if(len(moveCountermoveDict[g]) == 1):
                                    alreadyPaired.append(a)
                                    alreadyPaired.append(g)
                                    break
                        else:
                            moveCountermoveDict[a].append(g)
                if(len(moveCountermoveDict[a]) == 0):
                    isSingle.append(a)
        isWeaklyLost = True
        for move in moveCountermoveDict:
            if (move > 1):
                if(len(moveCountermoveDict[move]) == 0):
                    isWeaklyLost = False
                    break
        return isWeaklyLost
    
    def checkStronglyLostPosition(self, gaps):
        strongCountermove = {}
        for a in gaps:
            if(a > 1):
                strongCountermove[a] = []
                nextStage = self.pretendMove(gaps, a)
                for g in nextStage:
                    if(g > 1):
                        secondStage = self.pretendMove(nextStage, g)
                        weaklyLost = self.checkWeaklyLostPosition(secondStage)
                        if(weaklyLost[0]):
                            strongCountermove[a].append(g)
        isStrongLost = True
        for move in strongCountermove:
            if(move > 1):
                if(len(strongCountermove[move]) == 0):
                    isStrongLost = False
                    break
        return isStrongLost, strongCountermove
    
    def findWinningMove(self, gaps):
        possibleMatches = self.checkStronglyLostPosition(gaps)[1]
        for a in possibleMatches:
            if(len(possibleMatches[a]) == 0): 
                nextStage = self.pretendMove(gaps, a)
                if(self.checkWeak(nextStage) and a > 1):
                    return a
        return max(gaps)
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        if(len(movesPlayed) < 2):
            self.pairs = []
        if(len(self.pairs) > 0):
            if(len(self.pairs[0]) == 0):
                self.pairs = []
        movesPlayed = [int(i) for i in movesPlayed]
        remainingMoves = [i for i in remainingGaps]
        if((len(remainingMoves) < 50) and (len(remainingMoves) > 0) and (len(movesPlayed) != 0)):
            return self.findWinningMove(remainingMoves)
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