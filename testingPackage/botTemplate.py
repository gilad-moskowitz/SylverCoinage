class myNewBot:
    def __init__(self):
        #YOU CAN ADD A ML MODEL HERE TO INITIALIZE YOUR BOT
        pass
    
    def nextMove(self, movesPlayed, remainingGaps = []):
        #THE FUNCTION MUST RETURN A POSITIVE INTEGER
        #IF YOU RETRUN AN ILLEGAL MOVE YOU WILL LOSE
        #CURRENTLY THE "return 1" IS A PLACEHOLDER FOR YOUR ACTUAL MOVE
        
        if (len(movesPlayed) == 0):
            #TODO: WRITE YOUR CODE HERE TO PICK THE FIRST MOVE
            return 1
        #MAKES SURE YOUR BOT DOESN'T LOSE TRIVIALLY
        elif((3 in movesPlayed) and (2 not in movesPlayed)):
            return 2
        elif((2 in movesPlayed) and (3 not in movesPlayed)):
            return 3
        
        elif(len(movesPlayed) == 1):
            #TODO: WRITE THE CODE TO CHOOSE YOUR RESPONSE TO ANY OPENER (YOU MAY DELETE THIS IF YOU WANT)
            return 1
        
        else:
            #TODO: WRITE THE CODE TO RESPOND TO A GIVEN POSITION BEYOND THE FIRST AND SECOND MOVE
            return 1
