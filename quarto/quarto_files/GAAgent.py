import logging
import argparse
import random
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
import quarto
import quarto.objects2 as objects
from RandomPlayer import RandomPlayer

class GAAgent(quarto.Player):
    """player based on a Genetic Algorithm"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.game = quarto
        self.genome = None
        
    def set_genome(self, genome: list):
        '''
        GENOME EXPLICATION:
        genome[0] = tendency to put piece in longest row or to explore other sequences
        genome[1] = tendency to give the opponent the most present characteristics in the board or the least V
        genome[2] = tendency to favour diagonals over rows
        genome[3] = tendency to put the first piece on the edge or central cells V
        '''
        self.genome = genome

    def choose_piece(self) -> int:
        #return random.randint(0,15)
        board = self.get_game().get_board_status()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]
        in_board_pieces = [piece for piece in all_pieces if piece not in available_pieces]
        
        max_score = -1
        min_score = 10
        max_piece = None
        min_piece = None
        new_max = max_score
        new_min = min_score
        if available_pieces==all_pieces:
            return random.randint(0,15)
        for avail in available_pieces:
            scores = [self.piece_to_piece(avail, board_piece) for board_piece in in_board_pieces]
            if scores != []:
                new_max = max(scores)
                new_min = min(scores)
            if new_max > max_score:
                max_piece = avail
                max_score = new_max
            if new_min < min_score:
                min_piece = avail
                min_score = new_min
        return max_piece if random.random() < self.genome[1] else min_piece

    def place_piece(self) -> tuple[int, int]:
        board = self.get_game().get_board_status()
        sequence = self.longest_sequence()
        all_pieces = list(range(16))
        available_pieces = [piece for piece in all_pieces if piece not in board]

        if len(available_pieces)==(len(all_pieces)-1):
            if self.genome[3] > random.random():
                x = random.randint(1, 2)
                y = random.randint(1, 2)
                while board[x][y] == -1:
                    x = random.randint(1, 2)
                    y = random.randint(1, 2)
                    if board[1][1] != -1 & board[1][2] != -1 & board[2][2] != -1 & board[2][1] != -1:
                        print("arriva qui?")
                        return random.randint(0,3), random.randint(0,3)
                    return x, y
            else:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                i = 0
                while ((x in [1,2]) & (y in [1,2])): 
                    x = random.randint(0, 3)
                    y = random.randint(0, 3)
                    i*=1
                    if i > 30:
                        return random.randint(0,3), random.randint(0,3)
                return x, y

        if self.genome[2] > random.random():
            diag = sorted(sequence, key=lambda x: x[2], reverse=True)[0]
            if diag[1]!=4:
                if self.genome[0] > random.random():
                    diag_index = 1 - diag[0]
                else:
                    diag_index = diag[0]
                if diag_index==0:
                    diag = np.diag(np.array(board))
                if diag_index==1:
                    diag = np.diag(np.flip(np.array(board), 1))
                if self.piece_to_sequence(diag):
                    if diag_index==0:       
                        return np.where(diag == -1)[0][0], np.where(diag == -1)[0][0]
                    if diag_index==1:
                        return 3-np.where(diag == -1)[0][0], np.where(diag == -1)[0][0]     
                    
        if self.genome[0] > random.random():
            longest_row = sorted(sequence, key=lambda x: x[2])[0][0]
            i = 0
            row_index = 0 
            j = 0
            while i!=longest_row:
                i=random.randint(0,3)
                row_index = i
                j+=1
                if j > 30:
                    return random.randint(0,3), random.randint(0,3)
            j = 0
            pos = j
            while board[row_index, j] != -1:
                j=random.randint(0,3)
                pos = j
                if board[row_index, pos] != -1:
                    return random.randint(0,3), random.randint(0,3)
            return pos, row_index

        return random.randint(0,3), random.randint(0,3)

# UTILITIES

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
    
'''
/////////////
EVOLUTIONARY ALGORITHM
/////////////
'''
        
NUM_GENERATION = 25
POPULATION = 30
OFFSPRING = 10

def fitness(genome: list) -> float:
    game = quarto.Quarto()
    agent = GAAgent(game)
    agent.set_genome(genome)
    random = RandomPlayer(game)
    wins = 0
    flag = 50
    num_games = 40
    for n in range(num_games):
        game.reset()
        if flag == 1:
            game.set_players((agent, random))
            wins = (wins+1) if game.run_no_print()==0 else wins
            flag = 0
        else:
            game.set_players((random, agent))
            wins = wins if game.run_no_print()==0 else (wins+1)
            flag = 1                
    
    return wins/num_games

def mutation(genome):
    point = random.randint(0,len(genome)-1)
    genome[point]=random.random()
    return genome

def start_population():
    population = list()
    for genome in range(POPULATION):
        genome = [random.random() for  gene in range(4)]
        population.append((genome, fitness(genome)))
    return population    

def select_parent(population, tornament_size=10):
    '''select parent using a k = 10 tournament, takeing the one with best fitness'''
    return max(random.choices(population, k=tornament_size), key=lambda i: i[1])      

def genetic_algorithm(): 
    population = start_population()
    fitness_log = []
    for gen in tqdm(range(NUM_GENERATION)):
        offsprings = list()
        for i in range(OFFSPRING): 
            o = ()
            p = select_parent(population)
            o = mutation(p[0])
            offsprings.append((o, fitness(o)))
        population = population + offsprings   
        population = sorted(population, key=lambda i:i[1], reverse=True)[:POPULATION]
        fitness_log.append(population[0][1])
    plt.figure(figsize=(15, 6))
    plt.scatter(range(len(fitness_log)), fitness_log, marker=".")
    plt.title("Fitness log")
    plt.xlabel("Generation")
    plt.ylabel("win Rate")
    plt.show()
    best_sol = population[0][0]
    return best_sol

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
    genome = genetic_algorithm()  
    game = quarto.Quarto()
    agent = GAAgent(game)
    agent.set_genome(genome) 
    evaluate_n(game, agent, RandomPlayer(game))
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