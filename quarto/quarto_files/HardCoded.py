import logging
import argparse
import random
import quarto
import quarto.objects as objects

class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

class HardCodedPlayer(quarto.Player):
    """Player with hard-coded rules"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.game = quarto

    def choose_piece(self) -> int: 
        evaluate_board(self)
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)
    
    def evaluate_board(self) -> dict:
        board_eval = {}
        board = self.get_game().get_board_status()
        print(board)



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



def play_one(game: quarto.Quarto, p1: quarto.Player, p2: quarto.Player, num_games: int=1) -> None:

    game.reset()
    game.set_players((p1, p2))
    winner = game.run()
    logging.warning(f"Winner is player {winner}") 
    
def main():
    game = quarto.Quarto()
    #evaluate_n(game, HardCodedPlayer(game), main.RandomPlayer(game))
    play_one(game, HardCodedPlayer(game), RandomPlayer(game))

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