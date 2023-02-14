import copy
import logging
import argparse
import random
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
import quarto
import quarto.objects2 as objects
from RandomPlayer import RandomPlayer

class MinMaxAgent(quarto.Player):
    """player based on a Min Max kind of strategy"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.game = quarto

    def choose_piece(self) -> int:
        board = self.get_game().get_board_status()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]
    
        if available_pieces == all_pieces: return 0
        
        sequence = self.longest_sequence()
        return random.randint(0,15)
    
    def place_piece(self) -> tuple[int, int]:
        board = self.get_game().get_board_status()
        game = self.get_game()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]
        if len(available_pieces) == len(all_pieces)-1:
            return 0, 0
        
        minmax_game = QuartoMMAX()
        minmax_game.set_board(board)
        minmax_game.set_game(game)
        move = minmax_game.minmax_strategy()
        return move
    
#UTILITIES

    def evaluate_board(self) -> list:
        '''
        Returns a list of evaluation of the board based on number of elements
        on rows, columns and diagonal, in order to spot possible winning/losing combinations
        '''
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
        '''
        returns the longest row, column, and diagonal sorted from the longest to the shortest
        '''
        board_eval = self.evaluate_board()
        longest_list = []
        longest_list = [[np.argmax(board_eval[0]), np.max(board_eval[0]), 0], [np.argmax(board_eval[1]), np.max(board_eval[1]), 1], [np.argmax(board_eval[2]), np.max(board_eval[2]), 2]]
        longest = sorted(longest_list, key=lambda x: x[1], reverse=True)  
        return longest
    
    def piece_to_sequence(self, row: list) -> bool:
        '''
        evaluates the piece against a sequence (row, column or diagonal) and gives a score (0,1,2,3) to each piece already belonging to the 
        '''
        piece = self.game.get_selected_piece()
        scores = [self.piece_to_piece(piece, piece_row) for i, piece_row in enumerate(row) if piece_row != -1]
        if all(scores)>0 and len(scores)==3:
            return True
        else:
            return False

    def piece_to_piece(self, piece_1: quarto.Piece, piece_2: quarto.Piece) -> int:
        char_1 = (self.game.get_piece_charachteristics(piece_1)).binary
        char_2 = (self.game.get_piece_charachteristics(piece_2)).binary
        score = 0
        for i in range(len(char_1)):
            score=score+1 if char_1[i]==char_2[i] else score

        return score

class QuartoMMAX(quarto.Quarto):
    
    def __init__(self) -> None:
        super().__init__()
        
    def set_game(self, game):
        self.game = game

    def set_board(self, board):
        self.board = board

    def minmax_strategy(self) -> tuple[int, int]:
        tmp=self.game
        piece = tmp.get_selected_piece()
        state = None
        possible_state = self.possible_new_states(tmp, piece)
        for new_state, new_piece in possible_state:
            score = self.minmax_place(new_state, new_piece, is_maximizing=False)
            if score > 0:
                state = new_state
                break    
        return self.extract_move(state,tmp)
    
    def minmax_place(self, g, piece, is_maximizing, depth=0, bound=3):
        game = copy.deepcopy(g)
        def evaluate_minmax(is_maximizing):
            if game.check_winner()!= -1 or depth>bound:
                if game.check_winner()==0:
                    return  1 if is_maximizing else -1
                if game.check_winner()==1:
                    return  -1 if is_maximizing else 1
        if (score := evaluate_minmax(is_maximizing)) is not None: return score
        return (max if is_maximizing else min)(
            self.minmax_place(new_state[0], new_state[1], is_maximizing=not is_maximizing, depth=depth+1)
            for new_state in self.possible_new_states(game, piece))

    def possible_new_states(self, g, piece) -> list:

        possible_states = []
        board = g.get_board_status()
        all_pieces = list(range(16))
        available_pieces = [p for p in all_pieces if p not in board]
        available_pieces = [p for p in available_pieces if p!=piece]

        for i, row in enumerate(board):
            for j in range(len(row)):
                game = copy.copy(g)
                new_board = copy.copy(board)
                new_board[i, j] = piece if new_board[i, j] == -1 else board[i, j]
                if not (new_board==board).all():
                    for avail in available_pieces:
                        game._board = new_board
                        possible_states.append([game, avail])
        return possible_states
    
    def extract_move(self, state1, state2) -> tuple[int, int]:
        board1 = state1.get_board_status()
        board2 = state2.get_board_status()
        pos = np.where(board1!=board2)
        print(pos)
        return pos

'''   
/////////////
TESTING TOOLS
/////////////
'''
    
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
    #evaluate_n(game, MinMaxAgent(game), RandomPlayer(game))
    play_one(game, MinMaxAgent(game), RandomPlayer(game))

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