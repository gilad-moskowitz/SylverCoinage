import random
from numericalSemigroupLite import *

class myBot:
    def __init__(self):
        self.pPositions = [(2, 3), (4, 6), (4, 5, 6, 7), (4, 5, 11), (8, 12), (6, 9), (5, 7, 8), (4, 7, 13), (4, 9, 19), (5, 6, 19), (5, 9, 31), (6, 7, 16), (7, 9, 19), (7, 9, 24), (7, 10, 12), (4, 10), (6, 8, 10), (8, 10, 12, 14)]
    
    def minGenFunction(self, generators):
        allGens = sorted(list(set(generators)))
        for a in allGens:
            modo = [i%a for i in allGens]
            theEnd = int(len(allGens))
            start = 0
            while(start < theEnd):
                if(modo.index(modo[start]) != start):
                    modo.pop(start)
                    allGens.pop(start)
                    start = 0
                    theEnd = len(allGens)
                start += 1
        return sorted(list(set([i for i in allGens])))
    
    def checkForWin(self, minGens):
        for a in self.pPositions:
            for b in a:
                newCheck = [i for i in minGens]
                newCheck.append(b)
                newCheck = tuple(self.minGenFunction(newCheck))
                if ((newCheck == a) and (b not in minGens)):
                    return b
        return 0
    
    def coverRelations(self, gap):
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
    
    def possibleMoves(self, gaps):
        covering = self.coverRelations(gaps)
        potentials = []
        for a in covering:
            if((len(gaps) - len(covering[a]))%2 == 0):
                potentials.append(a)
        return potentials
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        movesPlayed = [int(i) for i in movesPlayed]
        minMoves = self.minGenFunction(movesPlayed)
        possibleWinningMove = self.checkForWin(minMoves)
        if(possibleWinningMove > 0):
            return possibleWinningMove
        remainingMoves = [i for i in remainingGaps]
        if(len(remainingGaps)>0):
            if((len(remainingMoves)%2) == 0):
                return (max(remainingMoves))
            else:
                linearCombos = [i for i in range(1, max(remainingMoves)) if i not in remainingMoves]
                j = len(remainingMoves) - 1
                while(j > 2):
                    for l in linearCombos:
                        if (((remainingMoves[j] - l) in remainingMoves) and ((remainingMoves[j] - l) > 3)):
                            return ((remainingMoves[j] - l))
                        else:
                            continue
                    j -= 1
                return (max(remainingMoves))
        if (len(movesPlayed) == 0):
            return random.choice([5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
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
            if(gcd_moves == 0):
                return random.randint(4, 30)
            else:
                newSet = [int(i/gcd_moves) for i in movesPlayed]
                if ((1 in newSet) and (gcd_moves > 1)):
                    return (gcd_moves*2 + 1)
                if(len(remainingGaps) == 0):
                    S = NumericalSemigroup(newSet)
                    remainingMoves = S.gaps
                else:
                    remainingMoves = [i for i in remainingGaps]
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