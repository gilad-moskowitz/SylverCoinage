import random
from numericalSemigroupLite import *

class testBot:
    def __init__(self):
        pass
    
    def nextMove(self, movesPlayed, remainingGaps, cap):
        movesPlayed = [int(i) for i in movesPlayed]
        if (len(movesPlayed) == 0):
            return random.choice([5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
        elif((3 in movesPlayed) and (2 not in movesPlayed)):
            return 2
        elif((2 in movesPlayed) and (3 not in movesPlayed)):
            return 3
        elif(len(movesPlayed) == 1):
            factors = PrimeFactorization(movesPlayed[0])
            if (len(factors) == 1):
                possible = [i for i in range(4, cap) if((i%movesPlayed[0]) != 0)]
                index = random.randint(0, len(possible) - 1)
                return possible[index]
            elif(max(factors) > 3):
                return max(factors)
            else:
                newMove = 1
                for a in factors:
                    newMove = newMove*a
                x = int(((newMove/min(factors)) + 1)*min(factors))
                if(x < cap):
                    return x
                else:
                    return 15
        else:
            gcd_moves = gcd_list(movesPlayed)
            if(gcd_moves > 1):
                newSet = [int(i/gcd_moves) for i in movesPlayed]
                if (1 in newSet):
                    return ((gcd_moves + 1))
                S = NumericalSemigroup(newSet)
                remainingMoves = S.gaps
                if((int((max(remainingMoves)*gcd_moves)) == 2) or (int((max(remainingMoves)*gcd_moves)) == 3)):
                    return ((gcd_moves*2 + 1))
                else:
                    maxIndex = len(remainingMoves) - 1
                    currentAttempt = int(remainingMoves[maxIndex]*gcd_moves)
                    while(currentAttempt > cap):
                        maxIndex -= 1
                        currentAttempt = int(remainingMoves[maxIndex]*gcd_moves)
                    return currentAttempt
            else:
                if (len(remainingGaps) == 0):
                    S = NumericalSemigroup(movesPlayed)
                    remainingMoves = S.gaps
                    maxIndex = len(remainingMoves) - 1
                    currentAttempt = int(remainingMoves[maxIndex]*gcd_moves)
                    while(currentAttempt > cap):
                        maxIndex -= 1
                        currentAttempt = int(remainingMoves[maxIndex]*gcd_moves)
                    return currentAttempt
                else:
                    maxIndex = len(remainingGaps) - 1
                    currentAttempt = int(remainingGaps[maxIndex]*gcd_moves)
                    while(currentAttempt > cap):
                        maxIndex -= 1
                        currentAttempt = int(remainingGaps[maxIndex]*gcd_moves)
                    return currentAttempt
