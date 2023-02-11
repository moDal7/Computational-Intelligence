# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto
from RandomPlayer import RandomPlayer

def evaluate_n(game: quarto.Quarto, p1: quarto.Player, p2: quarto.Player, num_games: int=100) -> None:
    
    wins = 0
    flag = 1
    
    for n in range(num_games):
        game.reset()
        if flag == 1:
            game.set_players((p1, p2))
            wins = (wins+1) if game.run_no_print()==0 else wins
            flag = 0
        else:
            game.set_players((p2, p1))
            wins = wins if game.run_no_print()==0 else (wins+1)
            flag = 1

    logging.warning(f"winning ratio of player1: {wins/num_games} over {num_games} games") 

def main():
    game = quarto.Quarto()
    evaluate_n(game, RandomPlayer(game), RandomPlayer(game))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()
