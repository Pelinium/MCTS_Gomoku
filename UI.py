import tkinter as tk
from rules import *

# citation: tkinter was borrowed from CMU 15-112: Fundamentals of Programming and Computer Science
# Class Notes: Graphics in Tkinter
class myGUI(tk.Frame):
    def __init__(self, parent):
        self.count = 0
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.grid_rowconfigure(1, weight = 1)
        self.parent.grid_columnconfigure(1, weight = 1)
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill = tk.X, padx = 5, pady = 5)
        self.board = [[0] * boardSize for i in range(boardSize)]
        self.newButtonArray = []
        self.mode = "prep"
        for i in range(boardSize):
            interMatrix = []
            for j in range(boardSize):
                btn = tk.Button(self.frame, text = '   ', command = lambda x = i, y = j: self.isClicked(x,y), relief = "sunken", fg = "BLUE", bg = "YELLOW")
                btn.grid(row = i, column = j)
                #btn.config(relief = "SUNKEN")
                interMatrix.append(btn)
            self.newButtonArray.append(interMatrix)
    def isClicked(self, x, y):
        if not self.mode == "pause" and not self.mode == "help":
            if isValidMove(self.board, x, y) == 1:
                if self.count % 2 == 1:  # change it if person v.s. AI
                    self.newButtonArray[x][y].config(text = "X")
                    m = 1
                else:
                    self.newButtonArray[x][y].config(text = "O")
                    m = 2
                self.count += 1
                self.board[x][y] = m
                result = isGameOver(self.board, m)
                if result != 0:
                    self.mode = "end"
                    if result == -1:
                        print("Game Over! The game ends as a tie!")
                    else:
                        print("Game Over! The winner is player", m, "!")
                        self.winner = m



#root=tk.Tk()
#app = myGUI(root)
#root.mainloop()


from tkinter import *

####################################
# init
####################################
root = Tk()

def init(data):
    # There is only one init, not one-per-mode
    data.app = myGUI(root)

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.app.mode == "prep"):         prepMousePressed(event, data)
    elif (data.app.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.app.mode == "pause"):      pauseMousePressed(event, data)
    elif (data.app.mode == "help"):       helpMousePressed(event, data)
    elif (data.app.mode == "end"):        endMousePressed(event, data)

def keyPressed(event, data):
    if (data.app.mode == "prep"):         prepKeyPressed(event, data)
    elif (data.app.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.app.mode == "pause"):      pauseKeyPressed(event, data)
    elif (data.app.mode == "help"):       helpKeyPressed(event, data)
    elif (data.app.mode == "end"):        endKeyPressed(event, data)

def redrawAll(canvas, data):
    if (data.app.mode == "prep"):         prepRedrawAll(canvas, data)
    elif (data.app.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.app.mode == "pause"):      pauseRedrawAll(canvas, data)
    elif (data.app.mode == "help"):       helpRedrawAll(canvas, data)
    elif (data.app.mode == "end"):        endRedrawAll(canvas, data)
####################################
# prep mode
####################################

def prepMousePressed(event, data):
    pass

def prepKeyPressed(event, data):
    if event.keysym == "s":
        data.app.mode = "playGame"


def prepRedrawAll(canvas, data):
    print(1)
    canvas.create_text(data.width/2, data.height/2-20,
                       text="Welcome to Gomoku!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2+20,
                       text="Press 's' key to start the game!", font="Arial 20")

####################################
# help mode
####################################

def helpMousePressed(event, data):
    pass

def helpKeyPressed(event, data):
    if event.keysym == "c":
        data.app.mode = "playGame"
    if event.keysym == "p":
        data.app.mode = "pause"



def helpRedrawAll(canvas, data):
    if data.app.mode == "help":
        canvas.create_rectangle(0,0,data.width,data.height,fill="red",width=0)

        canvas.create_text(data.width/2, data.height/2-70,
                       text="Gomoku Rules", font="Arial 24 bold")
        canvas.create_text(data.width/2, data.height/2,
                       text="Black plays first,and players alternately\n"
                            "placing a stone of their color \n"
                            "on an empty intersection.\n"
                            "The winner is the first player to get an\n"
                            "unbroken row of five stones \n"
                            "horizontally, vertically, or diagonally.", font="Arial 15")
        canvas.create_text(data.width/2, data.height/2+60,
                       text="Press 'c' to continue playing", font="Arial 15")
        canvas.create_text(data.width/2, data.height/2+80,
                           text="Press 'p' to pause the game", font="Arial 15")

####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
   # passo12都花
  #  1： o
  #  2: x
    pass

def playGameKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.app.mode = "help"
    elif (event.keysym == 'p'):
        if data.app.mode == "pause":
            data.app.mode = "playGame"
        else:
            data.app.mode = "pause"


def playGameRedrawAll(canvas, data):
    if data.app.mode == "playGame":
        canvas.create_text(data.width/2, data.height/2-40,
                       text="This could be challenging", font="Arial 26 bold")
        canvas.create_text(data.width/2, data.height/2-10,
                       text="Think before you make move", font="Arial 20")
        canvas.create_text(data.width/2, data.height/2+40,
                       text="Press 'h' for instructions!", font="Arial 20")
        canvas.create_text(data.width/2, data.height/2+60,
                       text="Press 'p' to have a break!", font="Arial 20")
        #画板


####################################
# pause mode
####################################

def pauseMousePressed(event, data):
    pass


def pauseKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.app.mode = "help"
    elif (event.keysym == 'c'):
        data.app.mode = "playGame"


def pauseRedrawAll(canvas, data):
    if data.app.mode == "pause":
        canvas.create_text(data.width/2, data.height/2-40,
                       text="Wanna stop for a while?", font="Arial 26 bold")
        canvas.create_text(data.width/2, data.height/2-10,
                       text="Let's have a break", font="Arial 20")
        canvas.create_text(data.width/2, data.height/2+ 10,
                       text="Click 'c' to go back to play", font="Arial 20")
        canvas.create_text(data.width/2, data.height/2+35,
                       text="Press 'h' for help!", font="Arial 20")

####################################


####################################
# end mode
####################################

def endMousePressed(event, data):
    pass

def endKeyPressed(event, data):
    if (event.keysym == 'r'):
        root = Tk()
        init(data)
    elif (event.keysym == 'h'):
        data.app.mode = "help"

def endRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2-40,
                       text="Game Over!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2-10,
                       text="Click 'r' 'to start again", font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+35,
                       text="Press 'h' for help!", font="Arial 20")
    if data.isGameOver == True:
        print("Game Over! The game ends as a tie!")
    else:
        print("Game Over! The winner is player", data.winner, "!")

####################################

def run(width=300, height=300):
    global root
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    #root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)