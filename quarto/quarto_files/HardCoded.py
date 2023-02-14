import logging
import argparse
import random
import numpy as np
from tqdm import tqdm
import quarto
import quarto.objects2 as objects
from RandomPlayer import RandomPlayer

class HardCodedPlayer(quarto.Player):
    '''
    Player with hard-coded rules
    '''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.game = quarto

    def choose_piece(self) -> int: 
        '''
        Hard coded method to choose a piece to give to the opponent
        '''
        board = self.get_game().get_board_status()
        all_pieces = range(16)
        available_pieces = [piece for piece in all_pieces if piece not in board]
        sequence = self.sorted_sequence()
        piece = self.choose_not_to_lose(available_pieces, sequence)
        return piece
    
    def place_piece(self) -> tuple[int, int]:
        '''
        Hard coded method to a position to place the piece.
        It analyzes all possible sequences in the board (rows, columns, diagonlas)
        It then checks if any sequence of 3 pieces is a winning sequence with the current given piece.
        If it's not, it fills any 3-piece-sequence to avoid an opponent to fill it with the next move.
        It then checks for sequences with len==2 and len==1. Based on the length of the sequence 
        and on the number of moves needed hypotetically to complete it, it places the piece on the sequence that
        gives the desired outcome.
        '''
        board = self.get_game().get_board_status()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]
        if len(available_pieces) == len(all_pieces)-1:
            return random.randint(0,1), random.randint(0,1)
        sequence = self.sorted_sequence()

        seq_len3 = [seq for seq in sequence if seq[1]==3]
        check_win = self.place_to_win(seq_len3)
        seq_len2 = [seq for seq in sequence if seq[1]==2]
        check_place2 = self.place_2(seq_len2)
        seq_len1 = [seq for seq in sequence if seq[1]==1]
        check_place1 = self.place_1(seq_len1)
        #checks if there is a sequence to win with the current given piece
        if len(seq_len3)!=0:
            if check_win[0]:
                return check_win[1], check_win[2]
         
        
        if seq_len2!=[]:
            if check_place2[0]:
                return check_place2[1], check_place2[2]
        
        if seq_len1!=[]:
            if check_place1[0]:
                return check_place1[1], check_place1[2]
        # anti-loop safety net
        return random.randint(0, 3), random.randint(0, 3)

    def choose_not_to_lose(self, pieces: list, sequence_list: list) -> int:
        '''
        looks for the worse piece for the current board state to give to the opponent
        if there is a winning piece for a sequence and a non-winning one, it chooses the non-winning one 
        '''
        max_score = 0
        piece_chosen = random.choices(pieces)[0] 
        seq_len3 = [seq for seq in sequence_list if seq[1]==3]
        seq_len2 = [seq for seq in sequence_list if seq[1]==2]
        seq_len1 = [seq for seq in sequence_list if seq[1]==1]

        for piece in pieces:
            all_zero_3 = True
            for seq in seq_len3:
                piece_scores = [self.piece_to_piece(piece, pi) for pi in seq]
                if 0 not in piece_scores:
                    all_zero_3 = False
            if all_zero_3:
                return piece

        for seq in seq_len2:
            for piece in pieces:
                piece_scores = [self.piece_to_piece(piece, pi) for pi in seq]
                new_max_score = max(piece_scores) if 0 not in piece_scores else 0
                if new_max_score > max_score:
                    max_score = new_max_score
                    piece_chosen = piece
            return piece_chosen
                
        for seq in seq_len1:
            for piece in pieces:
                piece_scores = [self.piece_to_piece(piece, pi) for pi in seq]
                if 0 in piece_scores:
                    return piece

        piece_chosen = random.choices(pieces)[0] 
        return piece_chosen

    def place_to_win(self, sequence: list) -> list:
        '''
        if the given piece and the board are a winnable situation, it wins
        '''
        board = self.get_game().get_board_status()
        for seq in sequence:
            if seq[1]==3:
                if seq[2] == 0:
                    row_index = seq[0]
                    row = board[row_index]
                    if self.piece_to_sequence(row):
                        return True, np.where(row == -1)[0][0], row_index
                
                if seq[2]==1:
                    col_index = seq[0]
                    col = np.array(board).T[col_index]
                    if self.piece_to_sequence(col):
                        return True, col_index, np.where(col == -1)[0][0]
                    
                if seq[2]==2:
                    diag_index = seq[0]
                    if diag_index==0:
                        diag = np.diag(np.array(board))
                    if diag_index==1:
                        diag = np.diag(np.flip(np.array(board), 1))
                    if self.piece_to_sequence(diag):
                        if diag_index==0:
                            return True, np.where(diag == -1)[0][0], np.where(diag == -1)[0][0]
                        if diag_index==1:
                            return True, (3-np.where(diag == -1)[0][0]), np.where(diag == -1)[0][0]

        # fill the only 3 sequence if there is not a winning move, to reduce winning probability of the opponent        
        if len(sequence)==1:
            for seq in sequence:
                if seq[1]==3:
                    if seq[2] == 0:
                        row_index = seq[0]
                        row = board[row_index]
                        return True, np.where(row == -1)[0][0], row_index
                    
                    if seq[2]==1:
                        col_index = seq[0]
                        col = np.array(board).T[col_index]
                        return True, col_index, np.where(col == -1)[0][0]
                        
                    if seq[2]==2:
                        diag_index = seq[0]
                        if diag_index==0:
                            diag = np.diag(np.array(board))
                            return True, np.where(diag == -1)[0][0], np.where(diag == -1)[0][0]
                        if diag_index==1:
                            diag = np.diag(np.flip(np.array(board), 1))
                            return True, (3-np.where(diag == -1)[0][0]), np.where(diag == -1)[0][0]
                   
        return False, random.randint(0, 3), random.randint(0, 3)


    def place_2(self, sequence: list) -> list:
        '''
        place position if considering the sequences of len==2
        '''
        board = self.get_game().get_board_status()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]
        for seq in sequence:
            if seq[1]==2:
                if seq[2] == 0:
                    row_index = seq[0]
                    row = board[row_index]
                    bad_piece_exists = False
                    for piece in available_pieces:
                        bad_piece_exists = True if min(self.piece_to_sequence_eval(row, piece))==0 else False
                    if self.piece_to_sequence(row, 2) & bad_piece_exists:
                        return True, np.where(row == -1)[0][0], row_index
                
                if seq[2]==1:
                    col_index = seq[0]
                    col = np.array(board).T[col_index]
                    bad_piece_exists = False
                    for piece in available_pieces:
                        bad_piece_exists = True if min(self.piece_to_sequence_eval(col, piece))==0 else False
                    if self.piece_to_sequence(col, 2) & bad_piece_exists:
                        return True, col_index, np.where(col == -1)[0][0]
                    
                if seq[2]==2:
                    diag_index = seq[0]
                    if diag_index==0:
                        diag = np.diag(np.array(board))
                    if diag_index==1:
                        diag = np.diag(np.flip(np.array(board), 1))
                    bad_piece_exists = False
                    for piece in available_pieces:
                        bad_piece_exists = True if min(self.piece_to_sequence_eval(diag, piece))==0 else False
                    if self.piece_to_sequence(diag, 2) & bad_piece_exists:
                        if diag_index==0:
                            return True, np.where(diag == -1)[0][0], np.where(diag == -1)[0][0]
                        if diag_index==1:
                            return True, (3-np.where(diag == -1)[0][0]), np.where(diag == -1)[0][0]
                    
        return False, random.randint(0, 3), random.randint(0, 3)
    
    def place_1(self, sequence: list) -> list:
        '''
        place position if considering the sequences of len==1
        '''
        board = self.get_game().get_board_status()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]

        for seq in sequence:
            if seq[1]==1:
                if seq[2] == 0:
                    row_index = seq[0]
                    row = board[row_index]
                    good_piece_exists = False
                    for piece in available_pieces:
                        good_piece_exists = True if min(self.piece_to_sequence_eval(row, piece))>=1 else False
                    if self.piece_to_sequence(row, 1) & good_piece_exists:
                        return True, np.where(row == -1)[0][0], row_index
                
                if seq[2]==1:
                    col_index = seq[0]
                    col = np.array(board).T[col_index]
                    good_piece_exists = False
                    for piece in available_pieces:
                        good_piece_exists = True if min(self.piece_to_sequence_eval(col, piece))>=1 else False
                    if self.piece_to_sequence(col, 1) & good_piece_exists:
                        return True, col_index, np.where(col == -1)[0][0]
                    
                if seq[2]==2:
                    diag_index = seq[0]
                    if diag_index==0:
                        diag = np.diag(np.array(board))
                    if diag_index==1:
                        diag = np.diag(np.flip(np.array(board), 1))
                    good_piece_exists = False
                    for piece in available_pieces:
                        good_piece_exists = True if min(self.piece_to_sequence_eval(diag, piece))>=1 else False
                    if self.piece_to_sequence(diag, 1) & good_piece_exists:
                        if diag_index==0:
                            return True, np.where(diag == -1)[0][0], np.where(diag == -1)[0][0]
                        if diag_index==1:
                            return True, (3-np.where(diag == -1)[0][0]), np.where(diag == -1)[0][0]
                    
        return False, random.randint(0, 3), random.randint(0, 3)
    
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
    
    def sorted_sequence(self) -> list:
        '''
        returns the longest sequences(rows, columns, and diagonals) sorted from the longest to the shortest and with an identifier 
        0 -> row
        1 -> column
        2 -> diagonal
        '''
        sequence_list = []
        
        board_eval = self.evaluate_board()
        for i, elem in enumerate(board_eval):
            for j, seq in enumerate(elem):
                sequence_list.append([j, seq, i])
        sequence_list = sorted(sequence_list, key=lambda x: x[1], reverse=True)
        return sequence_list
    
    def piece_to_sequence(self, row: list, target=3) -> bool:
        '''
        evaluates the piece against a sequence (row, column or diagonal) and returns a bool 
        '''
        piece = self.game.get_selected_piece()
        scores = [self.piece_to_piece(piece, piece_row) for i, piece_row in enumerate(row) if piece_row != -1]

        if all(scores)>0 and len(scores)==target:
            return True
        else:
            return False
        
    def piece_to_sequence_eval(self, row: list, piece) -> bool:
        '''
        evaluates the piece against a sequence (row, column or diagonal) and gives a score (0,1,2,3) to each piece already belonging to the 
        '''
        scores = [self.piece_to_piece(piece, piece_row) for i, piece_row in enumerate(row) if piece_row != -1]
        return scores

    def piece_to_piece(self, piece_1: quarto.Piece, piece_2: quarto.Piece) -> int:
        '''
        Evaluate a piece against another piece to return a "compatibility" score (number of common characters)
        '''
        char_1 = (self.game.get_piece_charachteristics(piece_1)).binary
        char_2 = (self.game.get_piece_charachteristics(piece_2)).binary
        score = 0
        for i in range(len(char_1)):
            score=score+1 if char_1[i]==char_2[i] else score

        return score
     
'''
/////////////
TESTING TOOLS
/////////////
'''
    
def evaluate_n(game: quarto.Quarto, p1: quarto.Player, p2: quarto.Player, num_games: int=100000) -> None:
    wins = 0
    flag = 1
    
    for n in tqdm(range(num_games)):
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
    #play_one(game, RandomPlayer(game), HardCodedPlayer(game))

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