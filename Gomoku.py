########################### Core Logic ##############################
import _thread
import socket
import string
import time

BLACK = "X"
WHITE = "O"
EMPTY = "."
BOARDSIZE = 7
DIFFICULTY = 800

def reversedColor(color):
    if color == EMPTY:
        return EMPTY
    if color == BLACK:
        return WHITE
    return BLACK


def initBoard(n):
    board = [[EMPTY] * n for _ in range(n)]
    return board


def toLetterCoord(n):
    return chr(ord('a') + n)


def fromLetterCoord(c):
    return ord(c) - ord('a')


def getColorName(color):
    if color == BLACK:
        return "black"
    elif color == WHITE:
        return "white"
    return ""


# Returns a board of n size, which should be even.
class Board(object):
    direction = ((1, 1), (1, 0), (0, 1), (1, -1))
    lengthToWin = 5

    def __init__(self, n):
        self.size = n
        self.data = initBoard(n)

    #
    def checkBoard(self):
        """
        Returns BLACK,WHITE if one of them wins,
        EMPTY if it is drawn, and None if the game should continue.
        :return:
        """
        for row in range(self.size):
            for col in range(self.size):
                c = self.__checkWin(row, col)
                if c is not None:
                    return c

        for row in range(self.size):
            for col in range(self.size):
                if self.data[row][col] == EMPTY:
                    return None  # should continue
        return EMPTY  # draw

    def __checkWin(self, row, col):
        color = self.data[row][col]
        if color == EMPTY:
            return None
        for (dx, dy) in Board.direction:
            x = row
            y = col
            count = -1
            while self.isInside(x, y) and self.getColor(x, y) == color:
                count += 1
                x += dx
                y += dy
            x = row
            y = col
            while self.isInside(x, y) and self.getColor(x, y) == color:
                count += 1
                x -= dx
                y -= dy
            if count >= Board.lengthToWin:
                return color
        return None

    def checkLegalMove(self, row, col, color):
        return self.isInside(row, col) and self.data[row][col] == EMPTY

    def isInside(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def getColor(self, row, col):
        return self.data[row][col]

    def putChess(self, row, col, color):
        if not self.checkLegalMove(row, col, color):
            raise RuntimeError("Illegal move")
        self.data[row][col] = color

    def hasValidMove(self, color):
        for row in range(self.size):
            for col in range(self.size):
                if self.checkLegalMove(row, col, color):
                    # print(f"Valid = {row},{col}")
                    return True
        return False


class Controller(object):
    """
    The controller for the game.
    Players and interface should be registered before calling startGame()
    """

    def __init__(self, n=BOARDSIZE):
        self.blackPlayer: Player = None
        self.whitePlayer: Player = None
        self.board: Board = Board(n)
        self.boardInterface: BoardInterface = None
        self.currentPlayerColor: string = EMPTY
        self.gameListeners = []
        pass

    def reInit(self, n):
        self.board = Board(n)
        pass

    def getPlayer(self, color):
        if color == WHITE:
            return self.whitePlayer
        elif color == BLACK:
            return self.blackPlayer
        return None

    def getCurrentPlayer(self):
        return self.getPlayer(self.currentPlayerColor)

    def __requirePlayerMove(self, color):
        self.currentPlayerColor = color
        player = self.getPlayer(color)
        player.requireMove(self.board, self)
        pass

    def putChess(self, player, row: int, col: int):
        """
        This method should only be called by player registered in the game.

        :param player: Player
        :param row:
        :param col:
        :return:
        """

        color = player.color
        board = self.board
        if not board.checkLegalMove(row, col, color):
            # print(f"INVALID : row= {row}, col= {col}")
            self.__endGame(GameEndEvent(reversedColor(color)))
            return
        board.putChess(row, col, color)
        possibleWinner = board.checkBoard()
        if possibleWinner is not None:
            self.__endGame(GameEndEvent(possibleWinner))
            return
        event = PutChessEvent(color, row, col)
        self.boardInterface.onPlayerMoved(event, board, self)
        nextColor = reversedColor(color)
        if board.hasValidMove(nextColor):
            self.__requirePlayerMove(nextColor)
        else:
            self.boardInterface.onSkipPlayer(self.getPlayer(reversedColor(color)), self)
            if not board.hasValidMove(color):
                self.__endGame(GameEndEvent(EMPTY))
                return
            self.__requirePlayerMove(color)
        pass

    def registerPlayer(self, player):
        color = player.color
        if color == WHITE:
            self.whitePlayer = player
        elif color == BLACK:
            self.blackPlayer = player
        pass

    def registerInterface(self, interface):
        self.boardInterface = interface
        pass

    def registerGameListener(self, listener):
        self.gameListeners.append(listener)
        pass

    def startGame(self, starter=BLACK):
        if self.blackPlayer is None or self.whitePlayer is None or self.boardInterface is None:
            raise RuntimeError("Players/Interface haven't been set!")
        self.boardInterface.onRefreshingBoard(self.board, self)
        self.currentPlayerColor = starter
        for listener in self.gameListeners:
            listener.onGameStarted(starter, self)
        if starter == WHITE:
            self.whitePlayer.requireMove(self.board, self)
        else:
            self.blackPlayer.requireMove(self.board, self)
        pass

    def __endGame(self, event):
        self.currentPlayerColor = EMPTY
        self.boardInterface.onGameEnded(event, self)
        for listener in self.gameListeners:
            listener.onGameEnded(event, self)

    def exceptionalEndGame(self, reason):
        return


class GameEndEvent(object):
    def __init__(self, winner, reason=None):
        self.winner = winner
        self.reason = reason

    pass


class PutChessEvent(object):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col


class Player(object):

    def __init__(self, color):
        self.color = color

    def requireMove(self, board, controller): pass

    def name(self):
        return getColorName(self.color)


class BoardInterface(object):
    def onPlayerMoved(self, event, board, controller): pass

    def onRefreshingBoard(self, board, controller): pass

    def onGameEnded(self, event, controller): pass

    def onSkipPlayer(self, player, controller): pass


########################### Bot Player ##############################


class AIPlayer(Player):

    @staticmethod
    def convertBlockCharToInt(ch):
        if ch == WHITE:
            return 1
        elif ch == BLACK:
            return 2
        else:
            return 0

    @staticmethod
    def convertBoardCharToInt(board):
        nBoard = [[0] * board.size for _ in range(board.size)]
        for i in range(board.size):
            for j in range(board.size):
                nBoard[i][j] = AIPlayer.convertBlockCharToInt(board.getColor(i,j))
        return nBoard

    def requireMove(self, board, controller):
        from mcts import returnBestMove
        (row, col) = returnBestMove(AIPlayer.convertBoardCharToInt(board), DIFFICULTY)
        controller.putChess(self, row, col)


######################### Command Line  ############################
class Struct(object):
    pass


_registered = []
_shouldEnd = Struct()
_shouldEnd.val = False


def regiser(func):
    _registered.append(func)


def stop():
    _shouldEnd.val = True


def mainLoop():
    timeGap = 0.2
    while not _shouldEnd.val:
        for f in _registered:
            f()
        time.sleep(timeGap)


class CommandLineHumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self.moveRequired = False
        self.controller = None
        regiser(self.tick)

    def requireMove(self, board, controller):
        self.moveRequired = True
        self.controller = controller
        pass

    def tick(self):
        if not self.moveRequired:
            return
        self.moveRequired = False
        while True:
            text = input(f"Enter move for {self.color} (RowCol):")
            if len(text) != 2 or text[0] not in string.ascii_lowercase \
                    or text[1] not in string.ascii_lowercase:
                print("Illegal format")
                continue
            row = fromLetterCoord(text[0])
            col = fromLetterCoord(text[1])
            self.controller.putChess(self, row, col)
            break


####################### Tkinter Interface ###########################
from tkinter import *


class TkinterInterface(BoardInterface):
    PVP = "PVP"
    PVE = "PVE"
    MAIN_MENU = 1
    IN_GAME = 2
    HELP_STAGE = 3
    CONNECTING = 4

    def __init__(self):

        self.width = None
        self.height = None
        self.timerDelay = None
        self.canvas = None
        self.controller = None

        self.stage = TkinterInterface.MAIN_MENU
        self.gameMode = TkinterInterface.PVE
        self.boardSize = BOARDSIZE
        self.selectedColor = BLACK

        self.tips = None
        self.moveRequired = False
        self.winEvent = None
        self.gameLasing = False

    # Blocked Method
    def run(self, width=500, height=500):
        def redrawAllWrapper(canvas):
            self.redrawAll(canvas)
            canvas.update()

        def mousePressedWrapper(event, canvas):
            self.mousePressed(event)
            redrawAllWrapper(canvas)

        def keyPressedWrapper(event, canvas):
            self.keyPressed(event)
            redrawAllWrapper(canvas)

        def timerFiredWrapper(canvas):
            self.timerFired()
            redrawAllWrapper(canvas)
            # pause, then call timerFired again
            canvas.after(self.timerDelay, timerFiredWrapper, canvas)

        self.__init()
        self.width = width
        self.height = height
        self.timerDelay = 100  # milliseconds
        root = Tk(className="Gomoku")
        root.resizable(width=False, height=False)  # prevents resizing window
        # create the root and the canvas
        canvas = Canvas(root, width=width, height=height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        self.canvas = canvas
        # set up events
        root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas))
        root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas))
        timerFiredWrapper(canvas)
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")
        pass

    def redrawAll(self, canvas):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, self.width, self.height,
                                fill="#F3E2A9", width=0)
        if self.stage == TkinterInterface.MAIN_MENU:
            self.mainMenuRedraw(canvas)
        elif self.stage == TkinterInterface.IN_GAME:
            self.gameStageRedraw(canvas)
        elif self.stage == TkinterInterface.HELP_STAGE:
            self.helpStageRedraw(canvas)
        elif self.stage == TkinterInterface.CONNECTING:
            self.connectingRedraw(canvas)
        pass

    def gameStageRedraw(self, canvas):
        width = self.width
        height = self.height
        font = "Arial 16"
        canvas.create_text(30, 30, text=self.gameMode, font=font, anchor=CENTER)
        canvas.create_text(30, 60, text="Turn:", font=font, anchor=CENTER)
        curPlayer = self.controller.getCurrentPlayer()
        if curPlayer is None:
            cpName = ""
        else:
            cpName = curPlayer.name()
        canvas.create_text(40, 90, text=cpName, font="Arial 20 bold", anchor=CENTER)
        board = self.controller.board

        marginX = 100
        marginY = 30
        blockSize = min((height - marginY - 10) // board.size, (width - marginX - 10) // board.size)

        xEnd = marginX + blockSize * board.size
        yEnd = marginY + blockSize * board.size
        for i in range(board.size + 1):
            x = marginX + blockSize * i
            y = marginY + blockSize * i
            canvas.create_line(marginX, y, xEnd, y)
            canvas.create_line(x, marginY, x, yEnd)

        block_2 = blockSize // 2
        block_6 = blockSize // 6
        block2_3 = blockSize * 2 // 3

        for i in range(board.size):
            x = marginX + blockSize * i + block_2
            y = marginY + blockSize * i + block_2
            t = toLetterCoord(i)
            canvas.create_text(x, marginY - 3, text=t, anchor=S)
            canvas.create_text(marginX - 7, y, text=t, anchor=E)
            x = marginX + blockSize * i + block_6
            for j in range(board.size):
                y = marginY + blockSize * j + block_6
                if board.getColor(i, j) == EMPTY:
                    continue
                color = getColorName(board.getColor(i, j))
                canvas.create_oval(x, y, x + block2_3, y + block2_3, fill=color, outline="black")
        if self.tips is not None:
            canvas.create_text(20, height - 30, text=self.tips, font=font, anchor=W)
        if not self.gameLasing:
            win = self.winEvent
            canvas.create_text(40, 110, text="Winner:", font=font, anchor=CENTER)
            winnerName = self.controller.getPlayer(win.winner).name()
            canvas.create_text(40, 150, text=winnerName, font="Arial 20 bold", anchor=CENTER)
            canvas.create_text(40, 220, text="R to \nrestart", font=font, anchor=CENTER)
        pass

    def mainMenuRedraw(self, canvas):
        width = self.width
        height = self.height
        font = "Arial 16"
        t = height / 2
        canvas.create_text(width / 2, 200, text="Gomoku", font="Arial 30 bold", anchor=CENTER)
        canvas.create_text(width / 2, t, text="Press s to start.", font=font, anchor=CENTER)
        canvas.create_text(width / 2, t + 30, text="Press h for help.", font=font, anchor=CENTER)
        canvas.create_text(width / 2, t + 60, text="Press E/P to select mode: " + self.gameMode, font=font,
                           anchor=CENTER)
        canvas.create_text(width / 2, t + 90, text=f"Up and Down to change board size:{self.boardSize}",
                           font=font, anchor=CENTER)
        canvas.create_text(width / 2, t + 120, text="X/O to choose color: " + getColorName(self.selectedColor),
                           font=font, anchor=CENTER)
        canvas.create_text(width / 2, t + 150, text="Online Game: n to be server, m to be client",
                           font=font, anchor=CENTER)
        pass

    def helpStageRedraw(self, canvas):
        width = self.width
        height = self.height
        font = "Arial 16"
        text = "Rules for Gomoku:\n" \
               "Black plays first, and players alternate in placing \n" \
               "a stone of their color on an empty intersection.\n" \
               "The winner is the first player to get\n" \
               "an unbroken row of five stones horizontally,\n" \
               "vertically, or diagonally.\n"
        canvas.create_text(width / 2, height / 2, text=text, font=font, anchor=CENTER)

    def connectingRedraw(self, canvas):
        width = self.width
        height = self.height
        font = "Arial 25"
        canvas.create_text(width / 2, height / 2, text=self.tips, font=font, anchor=CENTER)
        canvas.create_text(width / 2, height - 50, text="Press c to cancel.", font=font, anchor=CENTER)
        pass

    def mousePressed(self, event):
        if self.stage != TkinterInterface.IN_GAME or not self.moveRequired or not self.gameLasing:
            return
        board = self.controller.board
        width = self.width
        height = self.height
        marginX = 100
        marginY = 30
        blockSize = min((height - marginY - 10) // board.size, (width - marginX - 10) // board.size)
        x = event.x
        y = event.y
        row = (x - marginX) // blockSize
        col = (y - marginY) // blockSize
        if not board.isInside(row, col):
            return
        controller = self.controller
        color = controller.currentPlayerColor
        if not board.checkLegalMove(row, col, color):
            self.tips = "Invalid move"
            return
        self.moveRequired = False
        controller.putChess(controller.getPlayer(color), row, col)
        pass

    def keyPressed(self, event):
        if self.stage == TkinterInterface.MAIN_MENU:
            self.mainMenuKeyPressed(event)
        elif self.stage == TkinterInterface.IN_GAME:
            self.gameStageKeyPressed(event)
        elif self.stage == TkinterInterface.HELP_STAGE:
            self.helpStageKeyPressed(event)
        elif self.stage == TkinterInterface.CONNECTING:
            self.connectingPressed(event)
        pass

    def mainMenuKeyPressed(self, event):
        ch = event.char.lower()
        if ch == "s":
            self.startGame()
            return
        elif ch == "e":
            self.gameMode = TkinterInterface.PVE
            return
        elif ch == "p":
            self.gameMode = TkinterInterface.PVP
            return
        elif ch == "x":
            self.selectedColor = BLACK
            return
        elif ch == "o":
            self.selectedColor = WHITE
            return
        elif ch == "n":
            self.startOnlineGameServer()
            return
        elif ch == "m":
            self.startOnlineGameClient()
            return
        elif ch == "h":
            self.stage = TkinterInterface.HELP_STAGE
            return
        if event.keysym == "Up":
            if self.boardSize < 26:
                self.boardSize += 1
            return
        elif event.keysym == "Down":
            if self.boardSize > 4:
                self.boardSize -= 1
            return

    def gameStageKeyPressed(self, event):
        if event.char == "r":
            self.controller.exceptionalEndGame("Restart")
            self.stage = TkinterInterface.MAIN_MENU

    def helpStageKeyPressed(self, event):
        self.stage = TkinterInterface.MAIN_MENU

    def connectingPressed(self, event):
        if event.char in ("c", "C"):
            self.stage = TkinterInterface.MAIN_MENU

    def timerFired(self):
        pass

    def __init(self):
        self.gameMode = TkinterInterface.PVE
        self.moveRequired = False
        self.stage = TkinterInterface.MAIN_MENU
        self.boardSize = BOARDSIZE
        self.controller = None
        pass

    def __setupController(self, controller):
        self.controller = controller
        controller.registerInterface(self)

    def startGame(self):
        self.__setupGame()
        controller = Controller(self.boardSize)
        controller.registerInterface(self)
        self.controller = controller

        controller.reInit(self.boardSize)
        controller.registerPlayer(TkinterPlayer(self.selectedColor, self))

        rColor = reversedColor(self.selectedColor)
        if self.gameMode == TkinterInterface.PVE:
            controller.registerPlayer(AIPlayer(rColor))
        elif self.gameMode == TkinterInterface.PVP:
            controller.registerPlayer(TkinterPlayer(rColor, self))
        controller.startGame()

    def showConnecting(self, address, isHost):
        if isHost:
            self.tips = "Waiting connection on\n" \
                f"{address[0]}:{address[1]}"
        else:
            self.tips = "Trying to connect to\n" \
                f"{address[0]}:{address[1]}"
        self.stage = TkinterInterface.CONNECTING
        self.redrawAll(self.canvas)

    def __setupGame(self):
        self.stage = TkinterInterface.IN_GAME
        self.gameLasing = True
        self.winEvent = None
        self.tips = None

    # game info : boardSize color
    def startOnlineGameServer(self):
        try:
            addressText = self.popupBox("Host address?", "127.0.0.1 9000")
            t = addressText.split(" ")
            print("Server created!")
            address = (t[0], int(t[1]))
            self.showConnecting(address, True)
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.bind(address)
            sk.settimeout(0.5)

            def func():
                try:
                    sk.listen(1)
                    conn, addr = sk.accept()
                    sk.settimeout(None)
                    conn.send(bytes(f"{self.boardSize} {self.selectedColor}", "UTF-8"))

                    opponent = RemotePlayer(reversedColor(self.selectedColor), conn, True)
                    me = TkinterPlayer(self.selectedColor, self, "You")
                    controller = NetworkController(self.boardSize, conn, me, opponent)
                    self.controller = controller
                    controller.registerInterface(self)
                    print("Server starting!")

                    self.__setupGame()
                    controller.startGame()
                except:
                    if self.stage == TkinterInterface.CONNECTING:
                        self.canvas.after(500, func)
                    else:
                        print("Server closed!")
                        sk.close()

            self.canvas.after_idle(func)
        except:
            return

    def startOnlineGameClient(self):
        try:
            addressText = self.popupBox("Server address?", "127.0.0.1 9000")
            t = addressText.split(" ")
            address = (t[0], int(t[1]))
            print("Client connecting!")
            self.showConnecting(address, False)
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(0.5)

            def func():
                try:
                    sk.connect(address)
                    sk.settimeout(None)
                    gameInfo = str(sk.recv(100), "UTF-8").split(" ")
                    boardSize = int(gameInfo[0])
                    myColor = reversedColor(gameInfo[1])
                    opponent = RemotePlayer(reversedColor(myColor), sk, False)
                    me = TkinterPlayer(myColor, self, "You")
                    controller = NetworkController(boardSize, sk, me, opponent)
                    self.controller = controller
                    controller.registerInterface(self)
                    controller.currentPlayerColor = BLACK
                    print("Client connected!")

                    self.__setupGame()
                except:
                    if self.stage == TkinterInterface.CONNECTING:
                        self.canvas.after(500, func)
                    else:
                        print("Client disconnected!")
                        sk.close()

            self.canvas.after_idle(func())

        except:
            return

    def popupBox(self, info, default):
        from tkinter.simpledialog import askstring
        t = askstring("Enter address", info)
        if t is not None and len(t) == 0:
            return default
        return t

    def __markRefresh(self):
        self.canvas.after(0, self.redrawAll, self.canvas)

    def onPlayerMoved(self, event, board, controller):
        row = event.row
        col = event.col
        self.tips = f"Previous: {getColorName(event.color)} at {toLetterCoord(row) + toLetterCoord(col)}"

        self.__markRefresh()

    def onRefreshingBoard(self, board, controller):
        self.tips = None
        self.__markRefresh()

    def onGameEnded(self, event, controller):
        self.gameLasing = False
        self.winEvent = event
        self.moveRequired = False
        self.tips = event.reason
        self.__markRefresh()

    def onSkipPlayer(self, player, controller):
        self.tips = getColorName(player.color) + " is skipped"
        self.__markRefresh()


class TkinterPlayer(Player):
    def __init__(self, color, gui, name=None):
        super().__init__(color)
        self.gui = gui
        self.nameText = name

    def requireMove(self, board, controller):
        self.gui.moveRequired = True
        pass

    def name(self):
        if self.nameText is not None:
            return self.nameText
        return super(TkinterPlayer, self).name()


######################### Network connection ###############################
import socketserver


class NetworkController(Controller):
    """
    The controller for the game.
    Players and interface should be registered before calling startGame()
    """

    def __init__(self, n, sk, localPlayer, remotePlayer):
        super().__init__(n)
        self.blackPlayer: Player = None
        self.whitePlayer: Player = None
        self.localPlayer = localPlayer
        self.board: Board = Board(n)
        self.boardInterface: BoardInterface = None
        self.currentPlayerColor: string = EMPTY
        self.gameListeners = []
        self.sk: socket.socket = sk
        self.registerPlayer(localPlayer)
        self.registerPlayer(remotePlayer)
        _thread.start_new_thread(self.checkSocket, ())

    def checkSocket(self):
        while self.sk is not None:
            try:
                data = str(self.sk.recv(1024), 'ascii')
                if data == "require":
                    self.__requirePlayerMove(self.localPlayer.color)
                else:
                    t = data.split(" ")
                    row = int(t[0])
                    col = int(t[1])
                    color = t[2]
                    self.putChess(self.getPlayer(color), row, col)
            except:
                self.exceptionalEndGame("Other player exit!")

    def reInit(self, n):
        self.board = Board(n)
        pass

    def getPlayer(self, color):
        if color == WHITE:
            return self.whitePlayer
        elif color == BLACK:
            return self.blackPlayer
        return None

    def __requirePlayerMove(self, color):
        self.currentPlayerColor = color
        player = self.getPlayer(color)
        player.requireMove(self.board, self)
        pass

    def putChess(self, player, row: int, col: int):
        """
        This method should only be called by player registered in the game.

        :param player: Player
        :param row:
        :param col:
        :return:
        """
        if player == self.localPlayer:
            self.sk.send(bytes(f"{row} {col} {player.color}", "UTF-8"))
        color = player.color
        board = self.board
        if not board.checkLegalMove(row, col, color):
            # print(f"INVALID : row= {row}, col= {col}")
            self.__endGame(GameEndEvent(reversedColor(color)))
            return
        board.putChess(row, col, color)
        possibleWinner = board.checkBoard()
        if possibleWinner is not None:
            self.__endGame(GameEndEvent(possibleWinner))
            return
        event = PutChessEvent(color, row, col)
        self.boardInterface.onPlayerMoved(event, board, self)
        nextColor = reversedColor(color)
        if board.hasValidMove(nextColor):
            self.__requirePlayerMove(nextColor)
        else:
            self.boardInterface.onSkipPlayer(self.getPlayer(reversedColor(color)), self)
            if not board.hasValidMove(color):
                self.__endGame(GameEndEvent(EMPTY))
                return
            self.__requirePlayerMove(color)
        pass

    def registerPlayer(self, player):
        color = player.color
        if color == WHITE:
            self.whitePlayer = player
        elif color == BLACK:
            self.blackPlayer = player
        pass

    def registerInterface(self, interface):
        self.boardInterface = interface
        pass

    def registerGameListener(self, listener):
        self.gameListeners.append(listener)
        pass

    def startGame(self, starter=BLACK):
        if self.blackPlayer is None or self.whitePlayer is None or self.boardInterface is None:
            raise RuntimeError("Players/Interface haven't been set!")
        self.boardInterface.onRefreshingBoard(self.board, self)
        self.currentPlayerColor = starter
        for listener in self.gameListeners:
            listener.onGameStarted(starter, self)
        if starter == WHITE:
            self.whitePlayer.requireMove(self.board, self)
        else:
            self.blackPlayer.requireMove(self.board, self)
        pass

    def __endGame(self, event):
        if self.currentPlayerColor == EMPTY:
            # already ended
            return
        if self.sk is not None:
            self.sk.close()
            self.sk = None
        self.currentPlayerColor = EMPTY
        self.boardInterface.onGameEnded(event, self)
        for listener in self.gameListeners:
            listener.onGameEnded(event, self)

    def exceptionalEndGame(self, reason):
        self.__endGame(GameEndEvent(self.localPlayer.color, reason))


class RemotePlayer(Player):

    def __init__(self, color, sk, isServerSide):
        super().__init__(color)
        self.sk = sk
        self.isServerSide = isServerSide

    def requireMove(self, board, controller):
        if self.isServerSide:
            self.sk.send(bytes("require", "UTF-8"))

    def name(self):
        return "Other"

        
############################# RUN ####################################


def runGomokuGui():
    gui = TkinterInterface()
    gui.run(700, 700)


if __name__ == '__main__':
    # runReversi()
    runGomokuGui()
