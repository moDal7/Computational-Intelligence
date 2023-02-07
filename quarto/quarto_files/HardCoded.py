import logging
import argparse
import random
import numpy as np
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
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        sequence = self.longest_sequence()
        board = self.get_game().get_board_status()
        for seq in sequence:
            if seq[2] == 0:
                row_index = seq[0]
                row = board[row_index]
                print(f"row: -> {row}")
                if self.piece_to_sequence(row):
                    print("does it work?")
                    return row_index, row.index(-1)
                
        return random.randint(0, 3), random.randint(0, 3)
    
    def evaluate_board(self) -> list:
        board_rows = []
        board_col = []
        board_diag = [] 
        board = self.get_game().get_board_status()
        board_rows = [sum(position>-1) for position in board]
        board_col = [sum(position>-1) for position in np.array(board).T]
        diag1 = [sum(np.diag(np.array(board))>-1)]
        diag2 = [sum(np.diag(np.flip(np.array(board), 1))>-1)]
        board_diag = [diag1[0], diag2[0]]
        
        return board_rows, board_col, board_diag
    
    def longest_sequence(self) -> list:
        board_eval = self.evaluate_board()
        longest_list = []
        longest_list = [[np.argmax(board_eval[0]), np.max(board_eval[0]), 0], [np.argmax(board_eval[1]), np.max(board_eval[1]), 1], [np.argmax(board_eval[2]), np.max(board_eval[2]), 2]]
        longest = sorted(longest_list, key=lambda x: x[1], reverse=True)  

        return longest
    
    def piece_to_sequence(self, row: list) -> bool:
        piece = self.game.get_selected_piece()
        scores = [self.piece_to_piece(piece, piece_row) for i, piece_row in enumerate(row)]
        if all(scores)>0 & len(scores)==3:
            return True
        else:
            return False

    def piece_to_piece(self, piece_1: quarto.Piece, piece_2: quarto.Piece) -> int:
        char_1 = (self.game.get_piece_charachteristics(piece_1)).binary
        char_2 = (self.game.get_piece_charachteristics(piece_2)).binary
        score = 0
        for i in range(len(char_1)):
            score=score+1 if char_1[i]==char_2[i] else  score

        return score
    
def evaluate_n(game: quarto.Quarto, p1: quarto.Player, p2: quarto.Player, num_games: int=1000) -> None:
    
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

def play_one(game: quarto.Quarto, p1: quarto.Player, p2: quarto.Player) -> None:
    game.reset()
    game.set_players((p1, p2))
    winner = game.run()
    logging.warning(f"Winner is player {winner}") 
    
def main():

    game = quarto.Quarto()
    evaluate_n(game, HardCodedPlayer(game), RandomPlayer(game))
    #play_one(game, HardCodedPlayer(game), RandomPlayer(game))

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