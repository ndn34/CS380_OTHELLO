import math
import random

import game
import othello

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):
    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()
        if len(moves) == 0: return None # if there are no possible moves, return None

        return random.choice(moves) # return a random move

class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.depth = depth # save depth for minimax search

    def choose_move(self, state):
        moves = state.generateMoves()
        if len(moves) == 0: return None
        elif len(moves) == 1: return moves[0] # if there is only one move, return it
        isMax = state.nextPlayerToMove == othello.PLAYER1 # check if we are max or min

        bestMove = None
        if isMax:
            bestVal = float('-inf') # set best value to negative infinity if we are max
        else:
            bestVal = float('inf') # set best value to positive infinity if we are min
        for move in moves: #check each moves minimax value
            child = state.applyMoveCloning(move) #generate state after move
            val = self.minimax(child, self.depth-1, not isMax) # calculate minimax value
            if isMax and val > bestVal: # if its the best minimax score, save it
                bestVal = val
                bestMove = move
            elif not isMax and val < bestVal: # if its the min minimax score, save it
                bestVal = val
                bestMove = move
        return bestMove # return the best move

    def minimax(self, state, depth, maxmin):
        if depth == 0 or state.game_over(): # return score if depth is 0 OR game is won
            return state.score()

        moves = state.generateMoves()
        if len(moves) == 0:
            children = [state.applyMoveCloning(None)] # if no moves exist
        else:
            children = [state.applyMoveCloning(m) for m in moves] # otherwise generate all states after each move
        if maxmin: # check if we are max
            bestVal = float('-inf') # run through all child states
            for child in children:
                val = self.minimax(child, depth-1, False) # recursively call minimax on the child state
                bestVal = max(bestVal, val) # check if the value is better than the best value so far
            return bestVal
        else: # we are min
            bestVal = float('inf') # same as above but min now
            for child in children:
                val = self.minimax(child, depth-1, True) # recursively call minimax on the child state
                bestVal = min(bestVal, val)
            return bestVal

class AlphaBeta(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.depth = depth # save depth for minimax search

    def choose_move(self, state):
        moves = state.generateMoves()
        if len(moves) == 0: return None
        if len(moves) == 1: return moves[0] # if there is only one move, return it
        isMax = state.nextPlayerToMove == othello.PLAYER1 # check if we are max or min

        bestMove = None
        if isMax:
            bestVal = float('-inf') # set best value to negative infinity if we are max
        else:
            bestVal = float('inf') # set best value to positive infinity if we are min
        alpha = float('-inf') # set up alpha and beta for pruning
        beta = float('inf')
        for move in moves: #check each moves minimax value
            child = state.applyMoveCloning(move) #generate state after move
            val = self.alphabeta(child, self.depth-1, not isMax, alpha, beta) # calculate minimax value
            if isMax and val > bestVal: # if its the best minimax score, save it
                bestVal = val
                bestMove = move
                alpha = max(alpha, bestVal) # changing alpha to the best value so far
            elif not isMax and val < bestVal: # if its the min minimax score, save it
                bestVal = val
                bestMove = move
                beta = min(beta, bestVal) # changing beta to the best value so far
        return bestMove # return the best move

    def alphabeta(self, state, depth, maxmin, alpha, beta):
        if depth == 0 or state.game_over(): # return score if depth is 0 OR game is won
            return state.score()

        moves = state.generateMoves()
        if len(moves) == 0:
            children = [state.applyMoveCloning(None)] # if no moves exist
        else:
            children = [state.applyMoveCloning(m) for m in moves] # otherwise generate all states after each move
        if maxmin: # check if we are max
            bestVal = float('-inf') # run through all child states
            for child in children:
                val = self.alphabeta(child, depth-1, False, alpha, beta)
                bestVal = max(bestVal, val) # check if the value is better than the best value so far
                alpha = max(alpha, bestVal)
                if beta <= alpha: #prune if beta is less than or equal to alpha
                    break
            return bestVal
        else: # we are min
            bestVal = float('inf') # same as above but min now
            for child in children:
                val = self.alphabeta(child, depth-1, True, alpha, beta)
                bestVal = min(bestVal, val)
                beta = min(beta, bestVal) # changing beta to the best value so far
                if beta <= alpha: #prune if beta is less than or equal to alpha
                    break
            return bestVal