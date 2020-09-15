import termcolor
import math
import time
import minimax

#board is 8x7
# colors are : red:0 green:1 yellow:2 blue:3 magenta:4 grey:5
colorcode = ["red","green","yellow","blue","magenta","grey"]

def colorblock(color):
    color = colorcode[color]
    print(termcolor.colored("██", color),end="")


class Filler(object):
    def __init__(self,board, counter=0,player1tiles=None, player2tiles=None):
        self.board = board
        self.counter = counter

        self.player1tiles = [(0,6)]
        if player1tiles:
            self.player1tiles = player1tiles

        self.player1color = self.board[6][0]   # down-left


        self.player2tiles = [(7,0)]
        if player2tiles:
            self.player2tiles = player2tiles

        self.player2color = self.board[0][7]   # up-right

    def printboard(self):
        print('{0:<6d} {1} {2:>6d}'.format(len(self.player1tiles),'||', len(self.player2tiles)))
        for i in self.board:
            for j in i:
                colorblock(j)
            print()

    def updateboard(self,color,isPlayer1Turn):
        if isPlayer1Turn:
            for i in self.player1tiles:  # set color then check
                self.board[i[1]][i[0]] = color
                # check
                if not i[1]==0 and self.board[i[1]-1][i[0]] == color:
                    app = (i[0],i[1]-1)
                    if app not in self.player1tiles:
                        self.player1tiles.append(app)

                if not i[0]== len(self.board[0])-1 and self.board[i[1]][i[0]+1] == color:
                    app = (i[0]+1,i[1])
                    if app not in self.player1tiles:
                        self.player1tiles.append(app)


                if not i[1]==len(self.board)-1 and self.board[i[1]+1][i[0]] == color:
                    app = (i[0],i[1]+1)
                    if app not in self.player1tiles:
                        self.player1tiles.append(app)

                if not i[0]==0 and self.board[i[1]][i[0]-1] == color:
                    app = (i[0]-1,i[1])
                    if app not in self.player1tiles:
                        self.player1tiles.append(app)

        else:
            for i in self.player2tiles:  # set color\
                self.board[i[1]][i[0]] = color
                # check
                if not i[1]==0 and self.board[i[1]-1][i[0]] == color:
                    app = (i[0],i[1]-1)
                    if app not in self.player2tiles:
                        self.player2tiles.append(app)

                if not i[0]== len(self.board[0])-1 and self.board[i[1]][i[0]+1] == color:
                    app = (i[0]+1,i[1])
                    if app not in self.player2tiles:
                        self.player2tiles.append(app)

                if not i[1]==len(self.board)-1 and self.board[i[1]+1][i[0]] == color:
                    app = (i[0],i[1]+1)
                    if app not in self.player2tiles:
                        self.player2tiles.append(app)

                if not i[0]==0 and self.board[i[1]][i[0]-1] == color:
                    app = (i[0]-1,i[1])
                    if app not in self.player2tiles:
                        self.player2tiles.append(app)
        self.player1color = self.board[6][0]   # down-left
        self.player2color = self.board[0][7]   # up-right
        self.counter+=1

    def copyboard(self):
        newboard = []
        for i in self.board:
            newboard.append(i.copy())
        return Filler(newboard, self.counter, self.player1tiles.copy(), self.player2tiles.copy())

    def getscore(self):
        return len(self.player1tiles) - len(self.player2tiles)

    def evaluation(self):
        return self.getscore()*(1/self.counter)

    def gameover(self):
        if len(self.player1tiles) + len(self.player2tiles) == len(self.board)*len(self.board[0]):
            return True
        return False

    def getmoves(self):
        moves = []
        for i in range(6):
            if i != self.player1color and i != self.player2color:
                moves.append(i)
        return moves

def playerinput(inputvalues):
    inputvalues = [str(i) for i in inputvalues]
    while True:
        inp = input()
        if inp in inputvalues:
            return int(inp)


def bestmove(game, depth, maximizingPlayer):    # returns the move, the score, prediction , time it took
    now = time.time()

    bestmove = None
    if maximizingPlayer:
        bestscore = -math.inf
    else:
        bestscore = math.inf

    for move in game.getmoves():
        newboard = game.copyboard()
        newboard.updateboard(move, maximizingPlayer)
        score = minimax.minimax(newboard, depth, -math.inf, math.inf, not maximizingPlayer)

        if maximizingPlayer:
            if score > bestscore:
                bestscore = score
                bestmove = move
        else:
            if score < bestscore:
                bestscore = score
                bestmove = move

    newboard = game.copyboard()
    newboard.updateboard(bestmove, maximizingPlayer)
    winscore = minimax.winchance(newboard, depth, -math.inf, math.inf, not maximizingPlayer)

    bottime = time.time() - now
    return bestmove,bestscore,winscore,bottime

'''
# colors are : red:0 green:1 yellow:2 blue:3 magenta:4 grey:5
boardgijs = [[3, 1, 0, 3, 1, 3, 2, 1],
         [1, 0, 3, 1, 0, 4, 1, 3],
         [2, 3, 4, 0, 4, 3, 5, 2],
         [3, 4, 2, 4, 5, 4, 3, 1],
         [4, 1, 4, 2, 1, 0, 4, 3],
         [2, 0, 3, 4, 3, 5, 1, 4],
         [5, 4, 2, 0, 2, 4, 0, 1]]


# colors are : red:0 green:1 yellow:2 blue:3 magenta:4 grey:5
boardolaf =[[2, 5, 0, 2, 5, 4, 2, 4],
            [0, 4, 5, 3, 1, 2, 0, 1],
            [5, 0, 4, 0, 2, 0, 2, 4],
            [0, 1, 2, 1, 2, 3, 4, 0],
            [5, 3, 5, 3, 1, 4, 5, 1],
            [2, 1, 0, 5, 3, 2, 1, 4],
            [0, 4, 5, 2, 1, 5, 2, 5]]

game = Filler(boardgijs)

humanstarts = False
humanturn = True


print(game.getmoves())
while True:
    game.printboard()

    if humanturn:
        prstr = []
        moves = game.getmoves()
        for i in moves:
            prstr.append(f"{i} : {colorcode[i]}")
        print(", ".join(prstr))

        game.updateboard(playerinput(moves), humanstarts)
    else:
        move,score,points = bestmove(game, 7, not humanstarts)
        print(f"bot choose {colorcode[move]} with score : {round(score,2)} | time : {round(bottime,3)}")
        if humanstarts:
            if points > 0:
                print(f"Bot is losing by {points} points")
            elif points < 0:
                print(f"Bot is wining by {-points} points")
            else:
                print("Bot is drawing")
        else:
            if points < 0:
                print(f"Bot is losing by {-points} points")
            elif points > 0:
                print(f"Bot is wining by {points} points")
            else:
                print("Bot is drawing")

        game.updateboard(move, not humanstarts)

    if game.gameover():
        break

    humanturn = not humanturn
    #humanstarts = not humanstarts

print("Game has ended")
print(f"Player 1 has {len(game.player1tiles)} tiles")
print(f"Player 2 has {len(game.player2tiles)} tiles")
print(counter)
'''
