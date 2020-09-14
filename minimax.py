import math


def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or position.gameover():
        return position.evaluation()


    if maximizingPlayer:
        maxEval = -math.inf
        for child in position.getmoves():
            newboard = position.copyboard()
            newboard.updateboard(child, True)
            eval = minimax(newboard, depth-1,alpha,beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = math.inf
        for child in position.getmoves():
            newboard = position.copyboard()
            newboard.updateboard(child, False)
            eval = minimax(newboard, depth-1,alpha,beta, True)
            minEval = min(minEval, eval)
            beta = min(beta,minEval)
            if beta <= alpha:
                break
        return minEval

def winchance(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or position.gameover():
        return position.getscore()


    if maximizingPlayer:
        maxEval = -math.inf
        for child in position.getmoves():
            newboard = position.copyboard()
            newboard.updateboard(child, True)
            eval = winchance(newboard, depth-1,alpha,beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = math.inf
        for child in position.getmoves():
            newboard = position.copyboard()
            newboard.updateboard(child, False)
            eval = winchance(newboard, depth-1,alpha,beta, True)
            minEval = min(minEval, eval)
            beta = min(beta,minEval)
            if beta <= alpha:
                break
        return minEval
