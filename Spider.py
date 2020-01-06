import random

#TODO:  
#       README
#       Error Testing
#       better description of game


#Preset decks for the game
fullDeck = ["AH", "2H", '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', \
        "AD", "2D", '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', \
        "AC", "2C", '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', \
        "AS", "2S", '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'] * 2

halfDeck = ["AD", "2D", '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', \
        "AS", "2S", '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'] * 4
            
easyDeck = ["AS", "2S", '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS'] * 8

vals = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13, '1':1} #Added '1' for column testing

#initialization of global variables needed for each playthrough of the game
difficulty = ''
stack = [] #Tracks which cards still need dealt
board = [[]]*10  
free = [5]*4 +[4]*6 #Shows which card position index onward in each stack is free
completed = [] #completed suits
score = 500

def printBoard(): #This will only ever be called after a move, so I can keep this as a module
    global board, free
    
    #Boolean that none of the columns are done printing
    cols = [0]*10
    #Tracks current height of cards
    i = 0
    print("\x1b[1;35m1  2  3  4  5  6  7  8  9  T")
    #While some column is still printing:
    while cols != [1]*10:
        row = ''
        for c in range(10):
            if cols[c] == 1: #If the column is finished :
                row += '   '
            elif len(board[c]) == 0:  #edge case: the column is empty
                row += '\x1b[1;32m__ '
                cols[c] = 1
            else: #Otherwise (column is not finished)
                if i < free[c]: #If the card should not be shown
                    row += '\x1b[1;34mXX '
                else: #otherwise the card is exposed
                    if board[c][i][1] in "DH":
                        row += '\x1b[1;31m'
                    else:
                        row += '\x1b[0;0m'
                    row += board[c][i] + ' '
                    if i == len(board[c]) - 1: #mark if last card
                        cols[c] = 1
        print(row + '\x1b[0;0m')
        i += 1
        
    print()
    print()
    st = "\x1b[0;0mCompleted Stacks: "
    for i in range(len(completed)):
        if completed[i] in "DH":
            st += '\x1b[1;31m'+completed[i]+", "
        else:
            st += '\x1b[0;0m'+completed[i]+", "
    
    print(st)
    print("\x1b[0;0mDeals left: "+ str(len(stack) // 10))
    print("Score: "+str(score))
    return

#Starts a new game
def dealDeck():  
    global board, free, stack, difficulty, completed, score
    completed = []
    board = [[]]*10
    free = [5]*4 + [4]*6
    score = 500
    #Setting up which difficulty/deck the user wants, with user input error checking    
    while True:
        difficulty = input("Select difficulty (E for easy, M for medium, H for hard). Do not use punctuation: ")
        difficulty = str(difficulty).upper().strip()
        if (len(difficulty) == 1) and (difficulty in "EMH"):
            if difficulty == "E":
                stack = easyDeck.copy()
            elif difficulty == "M":
                stack = halfDeck.copy()
            else:
                stack = fullDeck.copy()
            break
        else:
            print("Sorry, invalid entry. Try again.")
        
    #Shuffle the playing deck
    random.shuffle(stack)
    
    #Deal out the cards by column
    for column in range(10):
        i = 0
        newColumn = []
        while i <= free[column]:
            newColumn.append(stack.pop())
            i += 1
        board[column] = newColumn
        
    return

#Deals out a row of cards from the deck (if available)
def dealRow():
    global board, stack, completed, score, free
    
    if stack == []:
        print("No more cards left to deal!")
        return
    score -= 1
    for i in range(10):
        dealt = stack.pop()
        board[i].append(dealt)
        if dealt[0] == 'A' and isComplete(board, free, i): #Check if complete only if an Ace is dealt
            board[i] = board[i][:len(board[i])-13]
            completed += [dealt[1]]
            score += 100
            if len(board[i]) == free[i] and free[i] != 0:
                free[i] -= 1
    return

#Prints a help message for the user
def printHelp():
    print("To move a card, use the format 'card column, top of stack to move, new column'  \
    (using 'T' for ten) Ex: '1, QS, T' to move a Queen of Spades from \
    the first column to the 10th column (columns go left to right). 1 point is taken for \
    every card move, and 100 points are awarded for completing a suit")
    return

#validates that the move specifications make sense (not that it is necessarily possible)
def validateMove(boardTemp, freeTemp, diff, col1, card, colMove):  
    
    global vals
    
    #starting with the card's current column
    if (len(col1) != 1) or (col1 not in "123456789T"):
        print("Invalid original column selection, try again.")
        return -1
    
    #then checking the card/if it is in that column
    if ((diff == "E") and (card not in easyDeck)) \
    or ((diff == "M") and (card not in halfDeck)) \
    or ((diff == "H") and (card not in fullDeck)):
        print("That card does not exist in this deck, try again.")
        return -1
    
    #Iterate through the column and see if the card can be moved
    colNum = vals[col1] - 1
    col = boardTemp[colNum]
    suit = card[1]
    prevCard = col[-1]
    colLen = len(col)
    
    cardLoc = colLen - 1 if prevCard == card else -1
        
    for i in range(-1, -1 * (colLen - freeTemp[colNum]) - 1, -1):
        currCard = col[i]
        
        if currCard == card:
            cardLoc = colLen + i
            break
        elif currCard[1] != suit:
            print("That card is buried in another suit")
            return -1
        elif i != -1 and vals[currCard[0]] != vals[prevCard[0]] + 1:
            print("That card is buried by an out of sequence card.")
            return -1
        prevCard = currCard
        
    if cardLoc == -1:
        print("That card does not exist in that column")
        return -1
    
    #and finally checking to see if the card can even be moved
    if (len(colMove) != 1) or (colMove not in "123456789T"):
        print("Invalid final column selection, try again.")
        return -1
    
    finCol = boardTemp[vals[colMove] - 1]
    if len(finCol) == 0 or vals[finCol[-1][0]] == vals[card[0]] + 1:
        return cardLoc  
    else:
        print("Error in final column")
        return -1
    
def moveStack(bTemp, fTemp, colCurr, cardIndex, colMove):
    
    boardTemp = bTemp.copy()
    freeTemp = fTemp.copy() 
    substack = boardTemp[colCurr][cardIndex:].copy()
    if cardIndex == freeTemp[colCurr] and freeTemp[colCurr] != 0: #Adjust free card tracker if necessary
        freeTemp[colCurr] -= 1 #deals out a new card
    
    boardTemp[colCurr] = boardTemp[colCurr][:cardIndex].copy()
    boardTemp[colMove] += substack
    
    return boardTemp, freeTemp
        
def isComplete(brd, fr, col):
    global vals
    
    if len(brd[col][fr[col]:]) < 13: #Need at least 13 cards to be a complete stack
        return False
    
    prevCard = brd[col][-1]
    if prevCard[0] != "A" or brd[col][-13][0] != "K": #to be complete, an Ace has to be on bottom of stack and a King on the top
        return False
    
    suit = prevCard[1]
    i = -2
    while i != -14: #Going as deep as needed:=
        currCard = brd[col][i] #extract the current card
        if currCard[1] != suit or vals[currCard[0]] != vals[prevCard[0]] + 1: #if the suit is off or not in order:
            return False 
        
        prevCard = currCard
        i -= 1
    print("Column Complete. Removing.")
        
    return True

def availableMoves(boardTemp, freeTemp):
    global vals
    
    #Get the bottom stacks from each column
    lastStacks = []
    topsOfStacks = []
    lastCards = []
    
    for column in range(10):
        if boardTemp[column] == []: #If the column is empty, no stack
            lastStacks.append([])
            topsOfStacks.append("__")
            lastCards.append("XX")
            continue
        
        prevCard = boardTemp[column][-1]
        lastCards.append(prevCard)
        colLen = len(boardTemp[column][freeTemp[column]:]) #how many cards are showing in this column
                
        i = -2
        suit = prevCard[1]
        while i * -1 != colLen + 1: #While there are still free cards to look at
            currCard = boardTemp[column][i]
            if currCard[1] != suit or vals[currCard[0]] != vals[prevCard[0]]+1: #if the suit does not match or out of order:
                lastStacks.append(boardTemp[column][i + 1:]) 
                topsOfStacks.append(boardTemp[column][i+1])
                break
            
            prevCard = currCard
            i -= 1
            
        if i * -1 == colLen + 1: #all revealed cards were in a stack
            lastStacks.append(boardTemp[column][i + 1:]) 
            topsOfStacks.append(boardTemp[column][i + 1]) 
            
    #Now have our bottom stacks

    moves = []
    for stack in range(10): #For each stack
        stackLen = len(lastStacks[stack]) #Get its length
        for card in range(stackLen): #For each card in that stack
            currCard = lastStacks[stack][card] #get the card info
            for last in range(10): #Checking each column
                #Moves to weed out (in order):
                #1) If we are looking at the same column as the stack
                #2) If we are moving to an empty column, manually enter that entry
                #3) If the values dont line up
                #4) If the current stack is already taller than it would be if the stack moved
                #5) If the new card is the same as the parent and out of suit order (most common looping condition)
                #6) If the card is not the top of its stack, dont worry about moving it, since 
                #   such a split would only be useful when moving to an empty column to switch out
                #   lengths of stacks of the same suit
                
                if stack == last: #If looking at the same column, continue
                    continue
                
                lastCard = lastCards[last] #Get the last card of this column
                if lastCard == "XX":
                    moves.append([stack, card - stackLen, last])
                    continue
                
                if vals[lastCard[0]] != vals[currCard[0]] + 1: 
                    continue
                
                if currCard[1] == lastCard[1] and not vals[topsOfStacks[stack][0]] < vals[topsOfStacks[last][0]]:          
                    continue
                
                colLen = len(boardTemp[stack])
                #if suits dont match and there are more cards in the column than just this stack, and some of those cards are showing and the card we are looking at is the same as the current stacks parent 
                if lastCard[1] != currCard[1] and colLen > stackLen and freeTemp[stack] + stackLen < colLen and lastCard == boardTemp[stack][-1 * stackLen - 1]:
                    continue
                
                if currCard[1] != lastCard[1] and card != 0:
                    continue
                
                #if all of these tests pass, then add this move to the possibilities
                moves.append([stack, card - stackLen, last]) #Middle value represents negative index in the stack where the card is moving from
    #additional output to make the user friendly suggestions            
    userFriendly = [[moves[i][0] + 1, boardTemp[moves[i][0]][moves[i][1]], moves[i][2] + 1] for i in range(len(moves))]
    #print(userFriendly) #For checking outside of hint function
    return (moves, userFriendly)

def hint(brd, fr):
    
    #Need to also check if the move results in a completed column
    global stack
        
    possMoves, userHelp = availableMoves(brd, fr)  
    numMoves = len(possMoves)
    cards = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'T':0,'J':0,'Q':0,'K':0}
    
    for i in range(numMoves):
        cards[userHelp[i][1][0]] += 1
    helpfulMoves = []
    
    for i in range(numMoves): #need a DFS of depth two to account for all loop possibilities
        #Get the current move we are looking at, the column we are moving from, the column we are moving to, and the index of the card to move
        
        board1 = []
        free1 = fr.copy()
    
        #Today I learned that the .copy() method does not work like I would like for 2-D arrays :)
        for j in range(10):
            board1.append(brd[j].copy())
            
        currMove = possMoves[i]
        col1 = currMove[0]
        col2 = currMove[2]
        indexOfMove = len(board1[col1]) + currMove[1] #index= column length + negative index value
        
        #Get the new board and free array for the move and get the available moves for THAT layout
        newBoard, newFree = moveStack(board1,free1,col1,indexOfMove,col2)
        newMoves, whoCares = availableMoves(newBoard,newFree)
        
        #First prune: If the move is to an empty column and the only available move after is to put it back, then ignore it
        if brd[col2] == [] and len(newMoves) == 1 and [newMoves[0][2],newMoves[0][1],newMoves[0][0]] == currMove:
            continue
        
        numMoves2 = len(newMoves)
        cards2 = {'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'T':0,'J':0,'Q':0,'K':0}
        for j in range(numMoves2):
            cards2[whoCares[j][1][0]] += 1
            
        loop = True
        
        #We can add moves that result in no more moves because that is still a gain that a loop
        #Would not provide (even if it does mean the user could lose)
        if numMoves2 == 0:
            helpfulMoves.append(userHelp[i])
            
        for j in range(numMoves2):
            currMove2 = newMoves[j]
            col12 = currMove2[0]
            col22 = currMove2[2]
            indexOfMove2 = len(newBoard[col12]) + currMove2[1]
            
            newBoardCopy = []
            newFreeCopy = newFree.copy()
            
            for k in range(10):
                newBoardCopy.append(newBoard[k].copy())
            
            newBoard2, newFree2 = moveStack(newBoardCopy, newFreeCopy, col12, indexOfMove2, col22)
            #dont care about the next moves from here
            
            #DFS of depth 2 to see if we are back where we started (goal #1)
            if newBoard2 == board1:
                continue
            
            loop = False
            
        #If there was a move that did not result in a repetition of the board, add it to the available moves
        if not loop:
            helpfulMoves.append(userHelp[i]) #add the userFriendly move since this is being returned to the user
        
        #Prune 2: if the number of moves is the same, and the same cards are involved  
        #if len(newMoves) == numMoves and True: #Add the second part of this later
         #   continue
        
    #If there are no possible moves and the stack is empty, the user can do nothing
    if helpfulMoves == [] and stack == []:
        print("It seems there is no possible way for you to win. Quit and try again.")
        return []
        
    return helpfulMoves #Change to random.choice(helpfulMoves) when comfortable

dealDeck()
while board != [[],[],[],[],[],[],[],[],[],[]]:
    printBoard()
    
    print("Chose a move or type 'D' to deal a row, 'I' for instructions, 'H' for a hint, 'N' for new game, or 'Q' to quit: ")
    move = input("")
    move = str(move).upper()
    #check to see if user needs help or wants to quit
    if move == "I":
        printHelp()
        input("Type ENTER to exit help")
        continue
    elif move == 'D':
        newDeal = 1
        #check if any columns are empty
        for column in board:
            if column == []:
                newDeal = 0
                break
        if not newDeal:
            print("Cannot deal a row if there is an empty column.")
            input("Press ENTER to continue")
            continue
        dealRow()
        #To allow the user to read the error message before moving on
        if stack == []:
            input("Press ENTER to continue")
            continue
        continue
    elif move == "H":
        print("One possibly helpful move: "+str(hint(board,free)))
        continue
    elif move == "Q":
        print("Thank you for playing, good-bye")
        break
    elif move == "N":
        dealDeck()
        continue  
    
    #check the input otherwise
    directions = move.split(",")
    
    if len(directions) != 3:
        print("Invalid input, try again.")
        continue
    
    (colCurr, card, colMove) = [item.strip() for item in directions]
    index = validateMove(board, free, difficulty, colCurr, card, colMove)
    if index == -1:
        input("Press enter to continue.")
        continue
  
    colCurr = vals[colCurr] - 1
    colMove = vals[colMove] - 1
    
    board, free = moveStack(board, free, colCurr, index, colMove)
    score -= 1
    
    if board[colMove][-1][0] == 'A' and isComplete(board, free, colMove): #Check if complete only if an ace was moved
        board[colMove] = board[colMove][:len(board[colMove])-13]
        completed += [card[1]]
        score += 100
        if len(board[colMove]) == free[colMove] and free[colMove] != 0:
            free[colMove] -= 1
    #_______________________________________________________________________________
    #If the game has been won, ask if the user wants to play again
    while board == [[],[],[],[],[],[],[],[],[],[]]:
        print("Congratulations, you win! Score: "+str(score))
        again = input("Play again? (Y for yes, N for no): ")
        again = str(again).upper()
        if again == "N":
            break
        if again == "Y":
            dealDeck()
            break
        else:
            print("Invalid entry. Try again")
            