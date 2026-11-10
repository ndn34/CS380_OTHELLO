import math
import random

import game

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
        self.depth = depth

    def choose_move(self, state):
        moves = state.generateMoves()

        return None

    def minimax(self, state, depth, maxmin):
        if depth == 0 or state.game_over():
            return state.score()

        if maxmin:
            bestVal = float('-inf')
            for child in [state.applyMoveCloning(move) for move in state.generateMoves()]:
                val = minimax(child, depth-1, False)

class AlphaBeta(game.Player):
    pass
