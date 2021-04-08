import random
from semigroupPackage import *
class testBot:
    def __init__(self):
        pass
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        if (len(movesPlayed) == 0):
            return random.randint(4, 30)
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
            if(gcd_moves > 1):
                newSet = [int(i/gcd_moves) for i in movesPlayed]
                if (1 in newSet):
                    return ((gcd_moves + 1))
                S = ListByGens(newSet)
                remainingMoves = gaps(S)
                if((int((max(remainingMoves)*gcd_moves)) == 2) or (int((max(remainingMoves)*gcd_moves)) == 3)):
                    return ((gcd_moves*2 + 1))
                else:
                    return int((max(remainingMoves)*gcd_moves))
            elif(gcd_moves == 0):
                return random.randint(4, 100)
            else:
                if (len(remainingGaps) == 0):
                    S = ListByGens(movesPlayed)
                    remainMoves = gaps(S)
                    return int(max(remainMoves))
                else:
                    return max(remainingGaps)
