import random
from numericalSemigroupLite import *

class maybeSolved:
    def __init__(self):
        self.pairs = []
        self.needToRecheck = False
    
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
    
    def singletons(self, gaps, alreadyPaired = []):
        covers = self.coverRelations(gaps)
        singles = []
        for a in gaps:
            isSingle = True
            for i in range(gaps.index(a) + 1, len(gaps)):
                if(gaps[i] not in covers[a]):
                    isSingle = False
                    break
            if(a in alreadyPaired):
                isSingle = False
            if(isSingle):
                singles.append(a)
        nonSingle = [g for g in gaps if g not in singles]
        if((len(nonSingle)%2 != 0) and (len(singles)>1)):
            singles.pop(1)
        return singles
    
    def pairings(self, gaps):
        singleLadies = self.singletons(gaps)
        tempGaps = [a for a in gaps if a > 1]
        newGaps = [b for b in gaps]
        covers = self.coverRelations(gaps)
        pairs = []
        alreadyPaired = []
        notPairs = []
        #FIRST PASS
        i = 0
        end = len(tempGaps)
        noNewSingles = True
        while(i < end):
            a = tempGaps[i]
            nextStage = self.pretendMove(newGaps, a)
            firstCheckFind = False
            if(len(alreadyPaired) > 0):
                covers = self.coverRelations(nextStage)
                for g in nextStage:
                    if((g > a) and (g not in alreadyPaired)):
                        remaining = [i for i in nextStage if((i > 1) and (i not in covers[g]) and (i != g))]
                        if(len(remaining)%2 != 0):
                            continue
                        isPairing = True
                        for b in remaining:
                            if(b not in alreadyPaired):
                                isPairing = False
                                break
                        if(isPairing):
                            pairs.append((a, g))
                            alreadyPaired.append(a)
                            alreadyPaired.append(g)
                            i = 0
                            tempGaps.pop(tempGaps.index(a))
                            tempGaps.pop(tempGaps.index(g))
                            end = len(tempGaps)
                            firstCheckFind = True
                            break
            if(not firstCheckFind):
                newSingles = self.singletons(nextStage, alreadyPaired)
            if(not firstCheckFind):
                for g in newSingles:
                    if(g in tempGaps):
                        pairs.append((a, g))
                        alreadyPaired.append(a)
                        alreadyPaired.append(g)
                        i = 0
                        tempGaps.pop(tempGaps.index(a))
                        tempGaps.pop(tempGaps.index(g))
                        end = len(tempGaps)
                        firstCheckFind = True
                        break
            if(not firstCheckFind):
                newTempGaps = [i for i in nextStage if i not in newSingles]
                if(len(newTempGaps)%2 == 1):
                    possibles = [i for i in newTempGaps if (i > a) and (i in tempGaps)]
                    if(len(possibles) == 0):
                        if(a not in notPairs):
                            notPairs.append(a)
                            newGaps = self.pretendMove(newGaps, a)
                            tempGaps = [i for i in newGaps if i > 1]
                            pairs = []
                            alreadyPaired = []
                            i = 0
                            end = len(tempGaps)
                        else:
                            i += 1
                        continue
                    pairs.append((a, min(possibles)))
                    alreadyPaired.append(a)
                    alreadyPaired.append(min(possibles))
                    i = 0
                    tempGaps.pop(tempGaps.index(a))
                    tempGaps.pop(tempGaps.index(min(possibles)))
                    end = len(tempGaps)
                else:
                    if(a not in notPairs):
                        notPairs.append(a)
                        newGaps = self.pretendMove(newGaps, a)
                        tempGaps = [i for i in newGaps if i > 1]
                        pairs = []
                        alreadyPaired = []
                        i = 0
                        end = len(tempGaps)
                    else:
                        i += 1
        newEnd = len(notPairs)
        while(newEnd>1):
            pairs.append((notPairs[0], notPairs[1]))
            notPairs.pop(0)
            notPairs.pop(0)
            newEnd = len(notPairs)
        return pairs, notPairs, singleLadies
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        if(len(movesPlayed) < 2):
            self.pairs = []
        if(len(self.pairs) > 0):
            if(len(self.pairs[0]) == 0):
                self.pairs = []
        movesPlayed = [int(i) for i in movesPlayed]
        remainingMoves = [i for i in remainingGaps]
        if((len(remainingMoves) < 100) and (len(remainingMoves) > 0) and (len(movesPlayed) != 0)):
            self.pairs = self.pairings(remainingMoves)
            if(len(self.pairs[1])>0):
                return min(self.pairs[1])
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
        #NORMAL STUFF
        elif((len(remainingMoves)>0) and (len(movesPlayed) != 0)):
            if(len(remainingMoves) < 100):
                self.pairs = self.pairings(remainingMoves)
                return self.nextMove(movesPlayed, remainingMoves)
            else:
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
            #USING THE PAIRING METHOD:
#         if(len(self.pairs) > 0):
#             for a in movesPlayed:
#                 i = 0
#                 end = len(self.pairs[0])
#                 while(i < end):
#                     duo = self.pairs[0][i]
#                     if(a in duo):
#                         for looking in duo:
#                             if(looking in remainingMoves):
#                                 print("Returning Duo: ", looking)
#                                 return looking
#                         self.pairs[0].pop(i)
#                         end = len(self.pairs[0])
#                     i += 1
#             if(len(self.pairs[1]) > 0):
#                 moveToPlay = min(self.pairs[1])
#                 print(moveToPlay)
#                 self.pairs[1].pop(0)
#                 if(len(self.pairs[1]) == 0):
#                     self.needToRecheck = True
#                 return moveToPlay
#             else:
#                 if((len(remainingMoves)%2) == 0):
#                     return max(remainingMoves)
#                 else:
#                     linearCombos = [i for i in range(1, max(remainingMoves)) if i not in remainingMoves]
#                     j = len(remainingMoves) - 1
#                     while(j > 2):
#                         for l in linearCombos:
#                             if (((remainingMoves[j] - l) in remainingMoves) and ((remainingMoves[j] - l) > 3)):
#                                 return (remainingMoves[j] - l)
#                             else:
#                                 continue
#                         j -= 1
#                     return max(remainingMoves)