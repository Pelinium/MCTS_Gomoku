#
# This file contains all methods for Monte Carlo Tree Search
#

# By default, the AI will move after you. AKA AI is the player 2
# The method used in my MCTS is UCB1 algorithm

from rules import *
import math
import random
from pandas import *

class MCTSnode:
    def __init__(self, myboard):
        #Constructor for non-root nodes
        self.children = []
        self.status = myboard
        self.prev = None
        self.playerNo = 1 # Who's turn
        self.wi = 0. # this node’s number of simulations that resulted in a win
        self.si = 0. #this node’s total number of simulation
        # The larger si is, the better result it will get.
        self.c = math.sqrt(2) # the factor by default

def getUCB1(node):
    if node.prev==None:
        return 0
    if node.si==0:
        return 0
    #if node.prev.si==0:
    #    return node.wi/node.si
    return node.wi/node.si+node.c*math.sqrt(np.log(node.prev.si)/node.si)

# Add a node to the parentNode with status as "newboard"
def add(parentNode, newboard, num):
    foundDiff = 0
    for i in range (0,boardSize):
        for j in range (0,boardSize):
            if parentNode.status[i][j]!=newboard[i][j]:
                foundDiff = 1
                break
        if foundDiff == 1:
            break

    if foundDiff == 0:
        # print("Cannot add")
        return

    childExist = 0
    for child in parentNode.children:
        if child.status[i][j] != 0:
            childExist = 1
            break

    if childExist == 0:
        temp = MCTSnode(newboard)
        temp.playerNo = num
        parentNode.children.append(temp)
        temp.prev = parentNode
        # m = runSimulationRandom(temp)
        m = runSimulationWithLightPlayout(temp)
        # Simulation to the interested node
        backPropagationPart1(temp)
        if m == 0:
            # The player on this node wins
            # Update the opponents node
            new = temp.playerNo%2+1
            backPropagationPart2(temp,new)
        if m == 1:
            # The opponents wins
            # Update this player's node
            new = temp.playerNo
            backPropagationPart2(temp,new)
    else:
        # m = runSimulationRandom(child)
        m = runSimulationWithLightPlayout(child)
        backPropagationPart1(child)
        if m == 0:
            new = child.playerNo%2+1
            backPropagationPart2(child,new)
        if m == 1:
            new = child.playerNo
            backPropagationPart2(child,new)

#Run one Simulation on a node
def runSimulationWithLightPlayout(MCTSnode):
    if isGameOver(MCTSnode.status, MCTSnode.playerNo) == MCTSnode.playerNo:
        return 0
    elif isGameOver(MCTSnode.status, MCTSnode.playerNo%2+1) == MCTSnode.playerNo%2+1:
        return 1
    tempBoard = [[0]*boardSize for i in range(boardSize)]
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            tempBoard[i][j] = MCTSnode.status[i][j]
    # Check If Any Move Make You Win
    # If no such move exist, make a random move
    while 1:
        listOfValidMove=[]
        for i in range (0, boardSize):
            for j in range (0, boardSize):
                if isValidMove(tempBoard,i,j):
                    newpair = [i,j]
                    tempBoard[i][j] = MCTSnode.playerNo
                    if isGameOver(tempBoard, MCTSnode.playerNo) == MCTSnode.playerNo:
                        return 0
                    #if winByDoubleFour(tempBoard, MCTSnode.playerNo) == 1:
                    #    return 0
                    else:
                        tempBoard[i][j] = 0
                        listOfValidMove.append(newpair)
        choice = random.choice(listOfValidMove)
        tempBoard[choice[0]][choice[1]] = MCTSnode.playerNo
        # print(DataFrame(tempBoard))
        if isGameOver(tempBoard, MCTSnode.playerNo) == MCTSnode.playerNo:
            # The simulated node's player wins
            return 0
        if isGameOver(tempBoard, MCTSnode.playerNo) == -1:
            return -1

        listOfValidMove=[]
        for i in range (0, boardSize):
            for j in range (0, boardSize):
                if(isValidMove(tempBoard,i,j)):
                    newpair = [i,j]
                    tempBoard[i][j] = MCTSnode.playerNo%2+1
                    if isGameOver(tempBoard, MCTSnode.playerNo%2+1) == MCTSnode.playerNo%2+1:
                        return 1
                    #if winByDoubleFour(tempBoard, MCTSnode.playerNo%2+1) == 1:
                    #  return 1
                    else:
                        tempBoard[i][j] = 0
                        listOfValidMove.append(newpair)
        choice = random.choice(listOfValidMove)
        tempBoard[choice[0]][choice[1]] = MCTSnode.playerNo%2+1
        # print(DataFrame(tempBoard))
        if isGameOver(tempBoard, MCTSnode.playerNo%2+1) == MCTSnode.playerNo%2+1:
            return 1
        if isGameOver(tempBoard, MCTSnode.playerNo%2+1) == -1:
            return -1

def runSimulationRandom(MCTSnode):
    if isGameOver(MCTSnode.status,MCTSnode.playerNo) == MCTSnode.playerNo:
        return 0
    if isGameOver(MCTSnode.status,MCTSnode.playerNo%2+1) == MCTSnode.playerNo%2+1:
        return 1
    # run one simulation on a node
    # Create a copy of myboard for simulation purpose
    tempBoard = [[0]*boardSize for i in range(boardSize)]
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            tempBoard[i][j] = MCTSnode.status[i][j]
    # Make random moves
    while 1:

        listOfValidMove=[]
        for i in range (0, boardSize):
            for j in range (0, boardSize):
                if isValidMove(tempBoard,i,j):
                    newpair = [i,j]
                    listOfValidMove.append(newpair)

        for m in range (0, boardSize):
            for n in range (0, boardSize):
                if tempBoard[m][n] == 0:
                    tempBoard[m][n] = MCTSnode.playerNo
                    if isGameOver(tempBoard,MCTSnode.playerNo) == MCTSnode.playerNo:
                        return 0
                    if winByDoubleFour(tempBoard, MCTSnode.playerNo) == 1:
                         return 0
                    else:
                        tempBoard[m][n] = 0

        choice = random.choice(listOfValidMove)
        tempBoard[choice[0]][choice[1]] = MCTSnode.playerNo
        if isGameOver(tempBoard, MCTSnode.playerNo) == -1:
            return -1


        listOfValidMove = []
        for i in range (0, boardSize):
            for j in range (0, boardSize):
                if(isValidMove(tempBoard,i,j)):
                    newpair = [i,j]
                    listOfValidMove.append(newpair)

        for m in range (0, boardSize):
            for n in range (0, boardSize):
                if tempBoard[m][n] == 0:
                    tempBoard[m][n] = MCTSnode.playerNo%2+1
                    if isGameOver(tempBoard,MCTSnode.playerNo%2+1) == MCTSnode.playerNo%2+1:
                        return 1
                    if winByDoubleFour(tempBoard, MCTSnode.playerNo%2+1) == 1:
                         return 1
                    else:
                        tempBoard[m][n] = 0

        choice = random.choice(listOfValidMove)
        tempBoard[choice[0]][choice[1]] = MCTSnode.playerNo%2+1
        if isGameOver(tempBoard, MCTSnode.playerNo%2+1) == -1:
            return -1
#Update the si value for the previous nodes
def backPropagationPart1(MCTSnode):
    if(MCTSnode == None):
        return
    else:
        MCTSnode.si += 1
        backPropagationPart1(MCTSnode.prev)
#Update the wi value for the previous nodes
def backPropagationPart2(MCTSnode,num):
    if(MCTSnode == None):
        return
    else:
        if(MCTSnode.playerNo == num):
            MCTSnode.wi += 1
        backPropagationPart2(MCTSnode.prev,num)


# By default, player 1 plays the game first
# The board here is assumed to be player two's turn
# For simiplicity, time is defined as number here.
def buildTree(myboard, time):
    root = MCTSnode(myboard)
    for i in range (0,time):
        selection(root,myboard,1)
        #printTree(root)
        print("Time is",i)
        #print("")
    return root

def isAllLegalMoveIncluedInSubroot(subroot,myboard):
    if len(subroot.children)==0:
        return 0
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            if isValidMove(myboard,i,j):
                # Expand the subroot with a random legal move
                flag = 0
                for child in subroot.children:
                    if child.status[i][j] == subroot.playerNo:
                        flag = 1
                        # Comfirm that the legal move is a child
                        break
                if flag == 0:
                    return 0
    return 1

# This method will expansion the current tree by one random move on a node of interest
def expansion(subroot,myboard,playerNum):
    # Make a copy of myboard to prevent pass by reference
    newboard = [[0]*boardSize for i in range(boardSize)]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            newboard[m][n] = myboard[m][n]
    # Make a random valid move
    listOfValidMove=[]
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            if(isValidMove(myboard,i,j)):
                newpair = [i,j]
                listOfValidMove.append(newpair)
    choice = random.choice(listOfValidMove)
    newboard[choice[0]][choice[1]] = playerNum
    add(subroot,newboard,playerNum%2+1)

def getLethalMove(subroot,myboard):
    newboard = [[0]*boardSize for i in range(boardSize)]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            newboard[m][n] = myboard[m][n]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            if newboard[m][n] == 0:
                newboard[m][n] = subroot.playerNo
                if isGameOver(newboard,subroot.playerNo) == subroot.playerNo:
                    newpair = [m,n]
                    return newpair
                else:
                    newboard[m][n] = 0
    newpair = [-1,-1]
    return newpair

def getOpponentLethalMove(subroot,myboard):
    newboard = [[0]*boardSize for i in range(boardSize)]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            newboard[m][n] = myboard[m][n]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            if newboard[m][n] == 0:
                newboard[m][n] = subroot.playerNo%2+1
                if isGameOver(newboard,subroot.playerNo%2+1) == subroot.playerNo%2+1:
                    newpair = [m,n]
                    return newpair
                else:
                    newboard[m][n] = 0
    newpair = [-1,-1]
    return newpair

def getOpponentLethalDoubleFourMove(subroot,myboard):
    newboard = [[0]*boardSize for i in range(boardSize)]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            newboard[m][n] = myboard[m][n]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            if newboard[m][n] == 0:
                newboard[m][n] = subroot.playerNo%2+1
                if winByDoubleFour(newboard,subroot.playerNo%2+1) == 1:
                    newpair = [m,n]
                    return newpair
                else:
                    newboard[m][n] = 0
    newpair = [-1,-1]
    return newpair

def getLethalDoubleFourMove(subroot,myboard):
    newboard = [[0]*boardSize for i in range(boardSize)]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            newboard[m][n] = myboard[m][n]
    for m in range (0, boardSize):
        for n in range (0, boardSize):
            if newboard[m][n] == 0:
                newboard[m][n] = subroot.playerNo
                if winByDoubleFour(newboard,subroot.playerNo) == 1:
                    newpair = [m,n]
                    return newpair
                else:
                    newboard[m][n] = 0
    newpair = [-1,-1]
    return newpair

def selection(subroot,myboard,playerNum):
    if isGameOver(myboard,1) != 0 or isGameOver(myboard, 2) != 0:
        return
    else:
        # Check if lethal move exist
        # When lethal move exist, it will always play the lethal move
        newpair = getLethalMove(subroot,myboard)
        # doubleFourPair = getLethalDoubleFourMove(subroot,myboard)
        if newpair[0] != -1 and newpair[1] != -1:
            #add(subroot,myboard,playerNum)
            newboard = [[0]*boardSize for i in range(boardSize)]
            for m in range (0, boardSize):
                for n in range (0, boardSize):
                    newboard[m][n] = myboard[m][n]
            newboard[newpair[0]][newpair[1]] = playerNum
            temp = MCTSnode(newboard)
            temp.playerNo = playerNum%2+1
            subroot.children.append(temp)
            backPropagationPart1(temp)
            new = temp.playerNo
            backPropagationPart2(temp,new)
            return
        '''elif doubleFourPair[0] != -1 and doubleFourPair[1] != -1:
            #add(subroot,myboard,playerNum)
            newboard = [[0]*boardSize for i in range(boardSize)]
            for m in range (0, boardSize):
                for n in range (0, boardSize):
                    newboard[m][n] = myboard[m][n]
            newboard[doubleFourPair[0]][doubleFourPair[1]] = playerNum
            temp = MCTSnode(newboard)
            temp.playerNo = playerNum%2+1
            subroot.children.append(temp)
            backPropagationPart1(temp)
            new = temp.playerNo
            backPropagationPart2(temp,new)
            return'''
        if isAllLegalMoveIncluedInSubroot(subroot,myboard) == 0:
            expansion(subroot,myboard,playerNum)
            return

        selectedChild = subroot.children[0]
        for child in subroot.children:
            if getUCB1(child) > getUCB1(selectedChild):
                selectedChild = child
        selection(selectedChild,selectedChild.status,playerNum%2+1)

def makeBestMove(myboard,time):
    myRoot = buildTree(myboard,time)
    newpair = getLethalMove(myRoot, myRoot.status)
    if newpair != [-1,-1]:
        myboard[newpair[0]][newpair[1]] = myRoot.playerNo%2+1

    selectedChild = myRoot.children[0]
    for child in myRoot.children:
        if child.wi/child.si > selectedChild.wi/selectedChild.si:
            selectedChild = child

    #Update board
    for i in range (0,boardSize):
        for j in range (0, boardSize):
            myboard[i][j] = selectedChild.status[i][j]

def returnBestMove(myboard,time):

    # Using three greedy algorithm to support the MCTS algorithm
    # Greedy 1
    # Make the move that makes you win
    rootCheck = MCTSnode(myboard)

    newpair = getLethalMove(rootCheck, rootCheck.status)
    if newpair != [-1,-1]:
        return newpair

    # Greedy 2
    # To quickly stop opponent from winning
    newpair = getOpponentLethalMove(rootCheck, rootCheck.status)
    if newpair != [-1,-1]:
        return newpair

    # Greedy 3
    # To stop opponent from getting a double four
    newpair = getOpponentLethalDoubleFourMove(rootCheck, rootCheck.status)
    if newpair != [-1,-1]:
        return newpair

    myRoot = buildTree(myboard,time)
    if(len(myRoot.children)==0):
        print("Tie!")
        return [-1,-1]
    selectedChild = myRoot.children[0]
    for child in myRoot.children:
        print("Child winning confidence,", child.wi/child.si)
        if child.wi/child.si > selectedChild.wi/selectedChild.si:
            selectedChild = child
    #Update board
    print ("IA winning confidence:",selectedChild.wi/selectedChild.si*100,"%")
    for i in range (0,boardSize):
        for j in range (0, boardSize):
            if myboard[i][j] != selectedChild.status[i][j]:
                newpair = [i,j]
                return newpair

def printTree(rootNode):
    print (rootNode.playerNo,"'s turn. ",rootNode.playerNo%2+1, "Winning rate:", rootNode.wi," / ",rootNode.si)
    print (DataFrame(rootNode.status))
    if len(rootNode.children) == 0:
        return
    else:
        for child in rootNode.children:
            printTree(child)