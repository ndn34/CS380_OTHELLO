import agent
import othello
import game
import sys
import re
import importlib
import os

def create_player(arg,  depht_or_time):
    if arg == 'human':
        return agent.HumanPlayer()
    elif arg == 'random':
        return agent.RandomAgent()
    elif arg == 'minimax':
        return agent.MinimaxAgent(depht_or_time)
    elif arg == 'alphabeta':
        return agent.AlphaBeta(depht_or_time)
    elif check_pattern(arg):
        if not os.path.exists(arg+ ".py"):
            print( "The agent is not defined in the systme!")
            exit()
        module = importlib.import_module(arg)
        my_agent = getattr(module, arg)
        return my_agent(depht_or_time)
    else:
        print( "The agent is not defined in the systme!")
        exit()

def check_pattern(text):
    """Checks if the text matches the pattern 'abc123'."""
    pattern = r'[a-z]{2,4}\d{2,4}'
    return re.match(pattern, text)

def get_arg(index, default=None):
    '''Returns the command-line argument, or the default if not provided'''
    return sys.argv[index] if len(sys.argv) > index else default

if __name__ == '__main__':

    initial_state = othello.State()

    if len(sys.argv) > 1:
        agent1 = sys.argv[1]
        agent2 = sys.argv[2]
        depht_or_time = 3
    if len(sys.argv) == 4 : 
        depht_or_time = int(sys.argv[3])        


    player1 = create_player(get_arg(1), depht_or_time)
    player2 = create_player(get_arg(2), depht_or_time)

    # player1 = agent.HumanPlayer()
    # player2 = agent.RandomAgent()

    game = game.Game(initial_state, player1, player2)

    game.play()

    