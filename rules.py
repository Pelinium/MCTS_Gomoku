#
# This file contains the basic rules of the game
#

# Define a function that check if the game ends
# Take in a 2D array, AKA a board
# By default, if tie happens, AI wins the game
howManyInLine = 3
boardSize = 3

board = [[0]*boardSize for i in range(boardSize)]

#Return the winner player num if the game is already over
#Return 0 if the game should continue
def isValidMove(myboard, i ,j):
    if(i>=0 and i<boardSize and j>=0 and j<boardSize):
        if(myboard[i][j] == 0):
            return 1
    return 0

# The method is used to check whether playerNum can win by doubleFour
# Return 0 if cannot win by double four
# Return 1 if can win by double four
# Step 1, check if the opponent can win in 1 move
def winByDoubleFour(myboard, playerNum):

    for m in range (0, boardSize):
        for n in range (0, boardSize):
            if myboard[m][n] == 0:
                myboard[m][n] = playerNum%2+1
                if isGameOver(myboard,playerNum%2+1) == playerNum%2+1:
                    return 0
                # Opponent can win in one move, so playerNum cannot win by double four
                else:
                    myboard[m][n] = 0

    # Finish checking
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            if myboard[i][j]!=0:

                #Check Left and Right ############################################################################
                flag1 = 0
                flag2 = 0
                countOfMaxInLine = 0
                tempj = j
                while tempj>=0:
                    if myboard[i][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempj -= 1
                    else:
                        break
                if tempj>=0:
                    if myboard[i][tempj] == 0:
                        flag1 = 1

                tempj = j+1
                while(tempj < boardSize):
                    if(myboard[i][tempj] == playerNum):
                        countOfMaxInLine += 1
                        tempj += 1
                    else:
                        break
                if tempj < boardSize:
                    if myboard[i][tempj] == 0:
                        flag2 = 1
                if countOfMaxInLine == howManyInLine - 1:
                    if flag1 == 1 and flag2 == 1:
                        return 1

                #Check Up and Down ############################################################################
                flag3 = 0
                flag4 = 0
                countOfMaxInLine = 0
                tempi = i
                while tempi>=0:
                    if myboard[tempi][j] == playerNum:
                        countOfMaxInLine += 1
                        tempi -= 1
                    else:
                        break
                if tempi>=0:
                    if myboard[tempi][j] == 0:
                        flag3 = 1

                tempi = i+1
                while tempi < boardSize:
                    if myboard[tempi][j] == playerNum:
                        countOfMaxInLine += 1
                        tempi += 1
                    else:
                        break
                if tempi < boardSize:
                    if myboard[tempi][j] == 0:
                        flag4 = 1
                if countOfMaxInLine == howManyInLine - 1:
                    if flag3 == 1 and flag4 == 1:
                        return 1

                #Check UpLeft and DownRight Corner ############################################################################
                flag5 = 0
                flag6 = 0
                countOfMaxInLine = 0
                tempi = i
                tempj = j
                while tempi >= 0 and tempj >= 0:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi -= 1
                        tempj -= 1
                    else:
                        break
                if tempi >= 0 and tempj >= 0:
                    if myboard[tempi][tempj] == 0:
                        flag5 = 1

                tempi = i+1
                tempj = j+1
                while tempi < boardSize and tempj < boardSize:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi += 1
                        tempj += 1
                    else:
                        break
                if tempi < boardSize and tempj < boardSize:
                    if myboard[tempi][tempj] == 0:
                        flag6 = 1
                if countOfMaxInLine == howManyInLine - 1:
                    if flag5 == 1 and flag6 == 1:
                        return 1


                #Check UpRight and DownLeft Corner ############################################################################
                flag7 = 0
                flag8 = 0
                countOfMaxInLine = 0
                tempi = i
                tempj = j
                while tempi>=0 and tempj < boardSize:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi -= 1
                        tempj += 1
                    else:
                        break
                if tempi>=0 and tempj < boardSize:
                    if myboard[tempi][tempj] == 0:
                        flag7 = 1
                tempi = i+1
                tempj = j-1
                while tempi < boardSize and tempj>=0:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi += 1
                        tempj -= 1
                    else:
                        break
                if tempi < boardSize and tempj>=0:
                    if myboard[tempi][tempj] == 0:
                        flag8 = 1
                if countOfMaxInLine == howManyInLine - 1:
                    if flag7 == 1 and flag8 == 1:
                        return 1
    return 0

def isGameOver(myboard, playerNum):
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            if myboard[i][j]!=0:

                #Check Left and Right
                countOfMaxInLine = 0
                tempj = j
                while(tempj>=0):
                    if myboard[i][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempj -= 1
                    else:
                        break

                tempj = j+1
                while(tempj < boardSize):
                    if(myboard[i][tempj] == playerNum):
                        countOfMaxInLine += 1
                        tempj += 1
                    else:
                        break
                if countOfMaxInLine >= howManyInLine:
                    return playerNum

                #Check Up and Down
                countOfMaxInLine = 0
                tempi = i
                while tempi>=0:
                    if myboard[tempi][j] == playerNum:
                        countOfMaxInLine += 1
                        tempi -= 1
                    else:
                        break
                tempi = i+1
                while tempi < boardSize:
                    if myboard[tempi][j] == playerNum:
                        countOfMaxInLine += 1
                        tempi += 1
                    else:
                        break
                if countOfMaxInLine>=howManyInLine:
                    return playerNum


                #Check UpLeft and DownRight Corner
                countOfMaxInLine = 0
                tempi = i
                tempj = j
                while tempi>=0 and tempj>=0:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi -= 1
                        tempj -= 1
                    else:
                        break
                tempi = i+1
                tempj = j+1
                while tempi < boardSize and tempj < boardSize:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi += 1
                        tempj += 1
                    else:
                        break
                if countOfMaxInLine >= howManyInLine:
                    return playerNum


                #Check UpRight and DownLeft Corner
                countOfMaxInLine = 0
                tempi = i
                tempj = j
                while tempi>=0 and tempj < boardSize:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi -= 1
                        tempj += 1
                    else:
                        break
                tempi = i+1
                tempj = j-1
                while tempi < boardSize and tempj>=0:
                    if myboard[tempi][tempj] == playerNum:
                        countOfMaxInLine += 1
                        tempi += 1
                        tempj -= 1
                    else:
                        break
                if countOfMaxInLine >= howManyInLine:
                    return playerNum
    tie = 1
    for i in range (0, boardSize):
        for j in range (0, boardSize):
            if myboard[i][j]==0:
                tie = 0
                break
        if tie == 0:
            break

    if tie == 1:
        return -1
    return 0
