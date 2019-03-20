#
# This file contains User Interface for Monte Carlo Tree Search
#

import tkinter as tk
from mcts import *

class myGUI(tk.Frame):

    def __init__(self,parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        #self.parent.grid_rowconfigure(1,weight=3)
        #self.parent.grid_columnconfigure(1,weight=3)
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        self.board = [[0]*boardSize for i in range(boardSize)]
        self.newButtonArray = []
        for i in range(0,boardSize):
            interMatrix = []
            for j in range(0,boardSize):
                btn = tk.Button(self.frame, text = '  ', command = lambda x=i, y=j: self.isClicked(x,y))
                btn.grid(row=i,  column=j)
                interMatrix.append(btn)
            self.newButtonArray.append(interMatrix)
        self.frame2 = tk.Frame(self.parent)
        self.frame2.pack(fill=tk.X, padx=10, pady=10)
        self.difficulty = tk.Scale(self.frame2,from_=0, to=2000,orient=tk.HORIZONTAL)
        self.difficulty.grid(row=0)
        self.difficulty.set(800)



    def isClicked(self,x,y):
        if(isValidMove(self.board, x ,y)==1):
            self.newButtonArray[x][y].config( text = "O" )
            self.board[x][y]=2
            if isGameOver(self.board,2) != 0:
                if(isGameOver(self.board,2)==-1):
                    print("Game Over! The game ends as a tie!")
                else:
                    print("Game Over! The winner is you!")
                exit(self)

            # IMPORTANT!!!!
            # Change this num to define the precision of simulation
            # pair = [x,y]
            newpair = returnBestMove(self.board,self.difficulty.get())
            # IMPORTANT!!!!
            if newpair == [-1,-1]:
                print("Tie!")
                exit(self)
            self.newButtonArray[newpair[0]][newpair[1]].config( text = "X" )
            self.board[newpair[0]][newpair[1]]=1
            if isGameOver(self.board,1) != 0:
                if(isGameOver(self.board,1)==-1):
                    print("Game Over! The game ends as a tie!")
                else:
                    print("Game Over! The winner is AI!")
                exit(self)
    def exit(self):
        self.frame.destroy()

root=tk.Tk()
app = myGUI(root)
root.mainloop()