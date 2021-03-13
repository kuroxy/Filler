from Filler import Filler, minimaxMove, mcts
import sys
import time



fillergame = Filler()
fillergame.reset()
if len(sys.argv) == 2:
        fillergame.getBoard(sys.argv[1], 1)

fillergame.boardprint()
while True:
    print("Colors 0:red 1:green 2:yellow 3:blue 4:purple 5:black | -1:(minimax) -2:(mcts)")
    userin = int(input())
    if userin == -1:
        oldtime = time.time()
        move,score = minimaxMove(fillergame, 11 , not fillergame.playerturn)
        print(f"(minimax) best move {move} with score {score} it took {round(time.time() - oldtime,3)} seconds")

        userin = int(input())
    if userin == -2:
        oldtime = time.time()
        move = mcts(fillergame, 500 , 40)
        print(f"(mcts) best move {move} it took {round(time.time() - oldtime,3)} seconds")

        userin = int(input())


    fillergame.turn(userin)
    fillergame.boardprint()

    if fillergame.gameover():
        break
