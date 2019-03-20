#
# Test file for no UI
#

from rules import *
from pandas import *

#Initialize the board with default value 9

print("Game Starts!")
while 1:
    print("Player1's turn")
    var1, var2 = input("Enter i and j here: ").split(" ")
    var1 = int(var1)
    var2 = int(var2)
    if isValidMove(board, var1, var2) == 1:
        board[var1][var2] = 1
    else:
        while 1:
            print("Invalid Move! Try again")
            var1, var2 = input("Enter i and j here: ").split(" ")
            var1 = int(var1)
            var2 = int(var2)
            if isValidMove(board, var1, var2) == 1:
                board[var1][var2] = 1
                break

    print(DataFrame(board))
    print("Player2's turn")
    if isGameOver(board, 1) == 1:
        print("Game Over! The Winner is Player 1!")
        break

    var1, var2 = input("Enter i and j here: ").split(" ")
    var1 = int(var1)
    var2 = int(var2)
    if isValidMove(board, var1, var2) == 1:
        board[var1][var2] = 2
    else:
        while 1:
            print("Invalid Move! Try again")
            var1, var2 = input("Enter i and j here: ").split(" ")
            var1 = int(var1)
            var2 = int(var2)
            if isValidMove(board, var1, var2) == 1:
                board[var1][var2] = 2
                break

    print(DataFrame(board))
    if isGameOver(board, 2) == 1:
        print("Game Over! The Winner is Player 2!")
        break