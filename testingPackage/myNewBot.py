import random
from numericalSemigroupLite import *

class myBot:
    def __init__(self):
        pass
    
    def nextMove(self, movesPlayed, remainingGaps = []):
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
