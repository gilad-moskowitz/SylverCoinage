import random
from numericalSemigroupLite import *

class myBot:
    def __init__(self):
        pass
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        movesPlayed = [int(i) for i in movesPlayed]
        if(len(remainingGaps)>0):
            remainingMoves = [i for i in remainingGaps]
            check4511 = [0, 0, 0]
            array4511 = [4, 5, 11]
            numberIn = 0
            for i in range(0, 3):
                if(array4511[i] in remainingMoves):
                    check4511[i] = 1
                    numberIn += 1
            if (numberIn == 1):
                if((6 not in movesPlayed) and (7 not in movesPlayed)):
                    for j in range(0,3):
                        if(check4511[j] == 1):
                            return int(array4511[j])
                elif((6 in movesPlayed) and (7 in movesPlayed)):
                    for j in range(0,3):
                        if(check4511[j] == 1):
                            return int(array4511[j])
                else:
                    pass
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
        elif((3 in movesPlayed) and (2 not in movesPlayed)):
            return 2
        elif((2 in movesPlayed) and (3 not in movesPlayed)):
            return 3
        if(len(movesPlayed) == 1 and 4 in movesPlayed):
            return 6
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
                    check4511 = [0, 0, 0]
                    array4511 = [4, 5, 11]
                    numberIn = 0
                    for i in range(0, 3):
                        if(array4511[i] in remainingMoves):
                            check4511[i] = 1
                            numberIn += 1
                    if (numberIn == 1):
                        if((6 not in movesPlayed) and (7 not in movesPlayed)):
                            for j in range(0,3):
                                if(check4511[j] == 1):
                                    return int(array4511[j])
                        elif((6 in movesPlayed) and (7 in movesPlayed)):
                            for j in range(0,3):
                                if(check4511[j] == 1):
                                    return int(array4511[j])
                        else:
                            pass
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