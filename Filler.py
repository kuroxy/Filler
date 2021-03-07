import numpy as np
import time
import random
import math

# 0     ,1      ,2      ,3      ,4      ,5
# R     ,L      ,Y      ,B      ,P      ,G
# red   ,lime   ,yellow ,blue   ,purple ,gray
# mapsize
#    8x7

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
            if self.board[pos[0]-1][pos[1]] == self.board[pos[0]][pos[1]] and visited[pos[0]-1][pos[1]] ==0:
                visited[pos[0]-1][pos[1]] = 1
                self.getNeigbours(visited, (pos[0]-1,pos[1]))

        if pos[0] < self.board.shape[0]-1:
            if self.board[pos[0]+1][pos[1]] == self.board[pos[0]][pos[1]] and visited[pos[0]+1][pos[1]] ==0:
                visited[pos[0]+1][pos[1]] = 1
                self.getNeigbours(visited, (pos[0]+1,pos[1]))

        if pos[1] > 0:
            if self.board[pos[0]][pos[1]-1] == self.board[pos[0]][pos[1]] and visited[pos[0]][pos[1]-1] ==0:
                visited[pos[0]][pos[1]-1] = 1
                self.getNeigbours(visited, (pos[0],pos[1]-1))
            
        if pos[1] < self.board.shape[1]-1:
            if self.board[pos[0]][pos[1]+1] == self.board[pos[0]][pos[1]] and visited[pos[0]][pos[1]+1] ==0:
                visited[pos[0]][pos[1]+1] = 1
                self.getNeigbours(visited, (pos[0],pos[1]+1))


    def countNeighbours(self, pos):
        visited = np.zeros(self.board.shape)
        self.getNeigbours(visited,pos)
        return visited.sum()


    def evaluation(self):
        return self.countNeighbours(self.playerpos[0]) - self.countNeighbours(self.playerpos[1])


    def fillNeighbours(self, pos, value):
        visited = np.zeros(self.board.shape)
        visited[pos[0]][pos[1]] = 1
        self.getNeigbours(visited,pos)
        inverted = np.logical_not(visited)
        self.board = self.board * inverted + visited*value


    def getAvailable(self):
        values = [0,1,2,3,4,5]
        values.remove(self.board[self.playerpos[0][0]][self.playerpos[0][1]])  # player 0 value
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
        for x in printboard:
            print(x)
        print()


    def copy(self):
        return Filler(self.board.copy(), self.playerturn)



def minimaxMove(game, depth, maximizingPlayer): # fillerclass , depth, True for player 0 else 1
    bestmove = None
    if maximizingPlayer:
        bestscore = -math.inf
    else:
        bestscore = math.inf

    for move in game.getAvailable():
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

    newboard = game.copy()
    newboard.turn(bestmove)
    return bestmove,bestscore


def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or position.gameover():
        return position.evaluation()


    if maximizingPlayer:
        maxEval = -math.inf
        for child in position.getAvailable():
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
        for child in position.getAvailable():
            newboard = position.copy()
            newboard.turn(child)
            eval = minimax(newboard, depth-1,alpha,beta, True)
            minEval = min(minEval, eval)
            beta = min(beta,minEval)
            if beta <= alpha:
                break
        return minEval


fillergame = Filler()
fillergame.boardprint()
while True:
    move,score = minimaxMove(fillergame, 10 , not fillergame.playerturn)
    print(f" best move {move} with score {score}")
    usermove = int(input())
    fillergame.turn(usermove)
    fillergame.boardprint()

    if fillergame.gameover():
        break
