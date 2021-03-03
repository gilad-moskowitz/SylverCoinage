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

#CODE FOR THE ACTUAL PACKAGE
class NumericalSemigroup: 
    
    def __init__(self, generators = []):
        self.gens = generators
        if(type(self.gens) != list):
            raise Exception("The input generators must be in the form of a list")
        if(len(self.gens) == 0):
            raise Exception("There must be at least one generator")
        try:
            self.gens = [int(i) for i in self.gens]
        except:
            "One of the given generators was not an integer."
        self.gens = sorted(list(self.gens))
        self.multiplicity = min(self.gens)
        self.elements = self.getElements(self.gens)
        self.gaps = [i*gcd_list(self.gens) for i in range(0, max(self.elements)) if ((i*gcd_list(self.gens) not in self.elements) and (i*gcd_list(self.gens) < max(self.elements)))]
        self.AperySetWithRespectToTheMultiplicity = self.AperySet(min(self.gens))
  
    def getElements(self, gens):
        currentCount = 0
        previousCount = 0
        newGennies = []
        List = [0]
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
        if(gcd_list(newGennies) != 1):
            newGennies2 = [int(i/gcd_list(newGennies)) for i in newGennies]
            upTo = max(newGennies2)*min(newGennies2)
            listOfElements = [i for i in newGennies2]
            elementz = []
            weStillHaveTime = True
            while (weStillHaveTime):
                for a in listOfElements:
                    elementz.append(a)
                listOfElements = SetAdd(listOfElements, newGennies2)
                elementz = sorted(list(set(elementz)))
                if(upTo in elementz):
                    for r in elementz:
                        currentCount += 1
                        if(r >= upTo):
                            break
                    if(currentCount == previousCount):
                        weStillHaveTime = False
                    else:
                        previousCount = int(currentCount)
                        currentCount = 0
        else:
            upTo = max(newGennies)*min(newGennies)
            listOfElements = [i for i in newGennies]
            elementz = []
            weStillHaveTime = True
            while (weStillHaveTime):
                for a in listOfElements:
                    elementz.append(a)
                listOfElements = SetAdd(listOfElements, newGennies)
                elementz = sorted(list(set(elementz)))
                if(upTo in elementz):
                    for r in elementz:
                        currentCount += 1
                        if(r >= upTo):
                            break
                    if(currentCount == previousCount):
                        weStillHaveTime = False
                    else:
                        previousCount = int(currentCount)
                        currentCount = 0
        for i in elementz:
            if(i > upTo):
                break
            List.append(int(i*gcd_list(newGennies)))
        gaps = [j for j in range(0, max(List)) if j not in List]
        if(len(gaps) < 1):
            frob = -1
        else:
            frob = max(gaps)
        return [element for element in List if element <= frob + min(newGennies)]

    def AperySet(self, n = -1, j = 1):
        if((type(n) != int) or n < 0):
            raise Exception("The Apery Set must be called with respect to a non-negative integer")
        if (j < 1):
            raise Exception("The j-th Apery set starts with j = 1.")
        jthSet = []
        for i in range(0, n):
            jCount = 0
            current = 0
            if(math.gcd(n, gcd_list(self.gens)) != 1):
                if(math.gcd(n, i) != gcd_list(self.gens)):
                    if(0 not in jthSet):
                        jthSet.append(0)
                    continue
            while(jCount < j):
                if(((current in self.elements) or ((current > max(self.elements)) and (current%gcd_list(self.gens) == 0))) and (current % n == i)):
                    jCount += 1
                    if(jCount == j):
                        break
                current += 1
            jthSet.append(current)
        return jthSet
    
    def Contains(self, n):
        if (math.gcd(n, gcd_list(self.gens)) != gcd_list(self.gens)):
            return False
        if (gcd_list(self.gens) == 1):
            return (int(n) >= self.AperySetWithRespectToTheMultiplicity[int(n)%self.multiplicity])
        else:
            newGens = [int(i/gcd_list(self.gens)) for i in self.gens]
            temp = NumericalSemigroup(newGens)
            newN = int(n/gcd_list(self.gens))
            return temp.Contains(newN)

    def minimalGenerators(self):
        miniGens = [i for i in self.gens]
        i = 0
        end = len(miniGens)
        while(i < end):
            restart = False
            for j in range(i + 1, end):
                if((miniGens[j] - miniGens[i]) in self):
                    miniGens.pop(j)
                    end = len(miniGens)
                    i = 0
                    restart = True
                    break
            if(not restart):
                i += 1
        return miniGens
    
    ### REDEFINING PROPERTIES ###
    def __eq__(self, other):
        return ((self.gaps == other.gaps) and (gcd_list(self.gens) == gcd_list(other.gens)))
    
    def __contains__(self, other):
        return self.Contains(other)
    
    def __repr__(self):
        return "Numerical semigroup generated by " + str(self.gens)
    
    
    
