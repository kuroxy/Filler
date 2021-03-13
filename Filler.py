import numpy as np
import time
import random
import math
from getmap import getmap
import sys
import termcolor

# 0     ,1      ,2      ,3      ,4      ,5
# R     ,L      ,Y      ,B      ,P      ,G
# red   ,lime   ,yellow ,blue   ,purple ,gray
# mapsize
#    8x7

colorcode = ["red","green","yellow","blue","magenta","grey"]

def colorblock(color):
    color = colorcode[color]
    print(termcolor.colored("██", color),end="")


class Filler():
    playerpos = ((0,6), (7,0))
    def __init__(self, board=None, playerturn=None):
        self.board = board
        self.playerturn = playerturn
        if board is None:
            self.reset()


    def reset(self, startingplayer=None):
        self.board = self.createBoard()
        self.playerturn = startingplayer if startingplayer else random.randrange(0,2)


    def createBoard(self, boardsize=(8,7)):
        board = np.zeros((boardsize))

        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                choices = [0,1,2,3,4,5]
                if x > 0 and board[x-1][y] in choices:
                    choices.remove(board[x-1][y]) # left 
                if y > 0 and board[x][y-1] in choices:
                    choices.remove(board[x][y-1]) # up
                board[x][y] = random.choice(choices)
        return board


    def getNeigbours(self,visited, pos):
        if pos[0] > 0:
            if visited[pos[0]-1][pos[1]] ==0:
                if self.board[pos[0]-1][pos[1]] == self.board[pos[0]][pos[1]]:
                    visited[pos[0]-1][pos[1]] = 1
                    self.getNeigbours(visited, (pos[0]-1,pos[1]))
                else:
                    visited[pos[0]-1][pos[1]] = 2
                

        if pos[0] < self.board.shape[0]-1:
            if visited[pos[0]+1][pos[1]] ==0:
                if self.board[pos[0]+1][pos[1]] == self.board[pos[0]][pos[1]]:
                    visited[pos[0]+1][pos[1]] = 1
                    self.getNeigbours(visited, (pos[0]+1,pos[1]))
                else:
                    visited[pos[0]+1][pos[1]] = 2
                
        if pos[1] > 0:
            if visited[pos[0]][pos[1]-1] ==0:
                if self.board[pos[0]][pos[1]-1] == self.board[pos[0]][pos[1]]:
                    visited[pos[0]][pos[1]-1] = 1
                    self.getNeigbours(visited, (pos[0],pos[1]-1))
                else:
                    visited[pos[0]][pos[1]-1] = 2

        if pos[1] < self.board.shape[1]-1:
            if visited[pos[0]][pos[1]+1] ==0:
                if self.board[pos[0]][pos[1]+1] == self.board[pos[0]][pos[1]]:
                    visited[pos[0]][pos[1]+1] = 1
                    self.getNeigbours(visited, (pos[0],pos[1]+1))
                else:
                    visited[pos[0]][pos[1]+1] = 2


    def countNeighbours(self, pos):
        visited = np.zeros(self.board.shape)
        self.getNeigbours(visited,pos)
        visited = visited==1
        return visited.sum()


    def evaluation(self):
        return self.countNeighbours(self.playerpos[0]) - self.countNeighbours(self.playerpos[1])


    def fillNeighbours(self, pos, value):
        visited = np.zeros(self.board.shape)
        visited[pos[0]][pos[1]] = 1
        self.getNeigbours(visited,pos)
        visited = visited==1
        inverted = np.logical_not(visited)
        self.board = self.board * inverted + visited*value


    def getAvailable(self):
        values = [0,1,2,3,4,5]
        values.remove(self.board[self.playerpos[0][0]][self.playerpos[0][1]])  # player 0 value
        if self.board[self.playerpos[1][0]][self.playerpos[1][1]] in values:
            values.remove(self.board[self.playerpos[1][0]][self.playerpos[1][1]])  # player 1 value
        return values


    def turn(self, value):
        if value in self.getAvailable():
            self.fillNeighbours(Filler.playerpos[self.playerturn], value)
            self.playerturn = not self.playerturn
        else:
            print("Invalid value")


    def gameover(self):
        if self.countNeighbours(self.playerpos[0]) + self.countNeighbours(self.playerpos[1]) == self.board.shape[0]* self.board.shape[1]:
            return True
        return False


    def boardprint(self):
        printboard = np.rot90(np.fliplr(self.board))
        for i in printboard:
            for j in i:
                colorblock(int(j))
            print()

        print()


    def copy(self):
        return Filler(self.board.copy(), self.playerturn)

    def loadBoard(self, board, playerstart):
        self.board = board
        self.playerturn = playerstart

    def getBoard(self, filename, playerstart):
        newboard = np.array(getmap(filename))
        rotatedboard = np.rot90(np.fliplr(newboard))
        self.loadBoard(rotatedboard, playerstart)


    def loadBoardString(self, mapstring, playerstart):
        newboard = np.array([ int(i) for i in mapstring])
        newboard = np.reshape(newboard, (7,8))
        rotatedboard = np.rot90(np.fliplr(newboard))
        self.loadBoard(rotatedboard, playerstart)


    def getNeigboursColor(self, player):    # player 0 or 1
        pos = self.playerpos[player]
        neighbourcolors = []
        visited = np.zeros(self.board.shape)
        self.getNeigbours(visited,pos)
        x,y = np.where(visited==2)
        av = self.getAvailable()

        for i in range(len(x)):
            if self.board[x[i]][y[i]] not in neighbourcolors and self.board[x[i]][y[i]] in av:
                neighbourcolors.append(self.board[x[i]][y[i]])
        if len(neighbourcolors) ==0:
            return av
        return neighbourcolors

    def getNeigboursColorvisi(self, player):    # player 0 or 1
        pos = self.playerpos[player]
        visited = np.zeros(self.board.shape)
        self.getNeigbours(visited,pos)

        return visited



def minimaxMove(game, depth, maximizingPlayer): # fillerclass , depth, True for player 0 else 1
    bestmove = None
    if maximizingPlayer:
        bestscore = -math.inf
    else:
        bestscore = math.inf

    allowmoves = game.getNeigboursColor(not maximizingPlayer)
    if len(allowmoves)==1:
        return allowmoves[0], None

    for move in allowmoves:
        newboard = game.copy()
        newboard.turn(move)
        score = minimax(newboard, depth, -math.inf, math.inf, not maximizingPlayer)

        if maximizingPlayer:
            if score > bestscore:
                bestscore = score
                bestmove = move
        else:
            if score < bestscore:
                bestscore = score
                bestmove = move

    return bestmove,bestscore


def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or position.gameover():
        return position.evaluation()


    if maximizingPlayer:
        maxEval = -math.inf
        for child in position.getNeigboursColor(not maximizingPlayer):
            newboard = position.copy()
            newboard.turn(child)
            eval = minimax(newboard, depth-1,alpha,beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = math.inf
        for child in position.getNeigboursColor(not maximizingPlayer):
            newboard = position.copy()
            newboard.turn(child)
            eval = minimax(newboard, depth-1,alpha,beta, True)
            minEval = min(minEval, eval)
            beta = min(beta,minEval)
            if beta <= alpha:
                break
        return minEval


def mcts(game, amount, depth):

    allowmoves = game.getNeigboursColor(game.playerturn)
    if len(allowmoves)==1:
        return allowmoves[0]

    moveeval = [0 for _ in range(len(allowmoves))]
    moveevalam = [0 for _ in range(len(allowmoves))]

    for moveindex,move in enumerate(allowmoves):
        newgamemove = game.copy()
        newgamemove.turn(move)

        if newgamemove.gameover(): 
            moveeval[moveindex] += newgamemove.evaluation()
            moveevalam[moveindex] += 1
            continue


        for _ in range(amount):
            gamecopy = newgamemove.copy()

            for _ in range(depth):
                ranmove = random.choice(gamecopy.getNeigboursColor(gamecopy.playerturn))
                gamecopy.turn(ranmove)
                if gamecopy.gameover():
                    break
            

            moveeval[moveindex] += gamecopy.evaluation()
            moveevalam[moveindex] += 1
    
    bestindex = 0
    

    if game.playerturn==0:
        bestval = -math.inf 
        for i in range(len(allowmoves)):
            moveeval[i] /= moveevalam[i]
            if moveeval[i] > bestval:
                bestval = moveeval[i]
                bestindex = i

    else:
        bestval = math.inf 
        for i in range(len(allowmoves)):
            moveeval[i] /= moveevalam[i]
            if moveeval[i] < bestval:
                bestval = moveeval[i]
                bestindex = i

    return allowmoves[bestindex]

