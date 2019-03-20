#
# Test file
#

from mcts import *

#Some test cases

#Test 1
board = [[0]*boardSize for i in range(boardSize)]
board[2][2] = 2
board[1][2] = 2
board[2][1] = 1
board[3][2] = 1
board[1][3] = 2
board[4][3] = 1
board[5][4] = 1
#board[1][0] = 2
print(DataFrame(board))
print(winByDoubleFour(board, 1))
#Test2
#board_ = [[0]*boardSize for i in range(boardSize)]
#board_[0][0]=1
#childNode = add(newNode,board_)'''
  
  
#Test3
#myRoot = buildTree(board,2)

#Test4
