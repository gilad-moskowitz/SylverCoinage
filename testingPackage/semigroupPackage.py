import math
#MATH FUNCTIONS NECESSARY:
def gcd_list(integers):
    listToUse = [i for i in integers]
    if (len(listToUse) == 0):
        return 0
    if (len(listToUse) == 1):
        return listToUse[0]
    while (len(listToUse) > 2):
        listToUse.append(math.gcd(listToUse[0], listToUse[1]))
        listToUse.pop(0)
        listToUse.pop(0)
    return math.gcd(listToUse[0], listToUse[1])

def PrimeFactorization(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


#SEMIGROUP FUNCTIONS:
def SetAdd(L1, L2):
    L3 = []
    for a in L1:
        for b in L2:
            L3.append(a+b)
    L3 = list(set(L3))
    return L3
    
def ListByGens(gens):
    currentCount = 0
    previousCount = 0
    newGennies = []
    finalList = []
    for t in range(0, len(gens)):
        isGen = True
        for y in range(0, len(gens)):
            if(gens[y] == gens[t]):
                continue
            if(int(gens[t])%int(gens[y]) == 0):
                isGen = False
                break
        if(isGen):
            newGennies.append(int(gens[t]))
    if(len(newGennies) < 2 or gcd_list(newGennies) != 1):
        return finalList
    Frob = max(newGennies)*min(newGennies)
    listOfElements = [i for i in newGennies]
    elementz = []
    weStillHaveTime = True
    while (weStillHaveTime):
        for a in listOfElements:
            elementz.append(a)
        listOfElements = SetAdd(listOfElements, newGennies)
        elementz = sorted(list(set(elementz)))
        if(Frob in elementz):
            for r in elementz:
                currentCount += 1
                if(r >= Frob):
                    break
            if(currentCount == previousCount):
                weStillHaveTime = False
            else:
                previousCount = int(currentCount)
                currentCount = 0
    for i in elementz:
        if(i > Frob):
            break
        finalList.append(i)
    return finalList
    
def gaps(Semigroup):
    return [i for i in range(1, max(Semigroup)) if i not in Semigroup]