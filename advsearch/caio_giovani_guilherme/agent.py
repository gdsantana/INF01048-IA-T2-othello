import random
import sys
from othello.board import Board
import copy
# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

class Node:
    def __init__(self, board, p_color, parent=None,cost=1,color = Board.WHITE, evaluation = 1,previous_move = (-1,-1), best_move = (-1,-1)):
        self.board = board
        self.player_color = p_color  
        self.parent = parent
        self.cost = cost
        self.color = color 
        self.eval = evaluation 
        self.previous_move = previous_move  
        self.best_move = best_move  

def expande(self):
        result = []
        moves = self.board.legal_moves(self.color)
        for move in moves:
            board = copy.deepcopy(self.board)
            board.process_move(move,self.color)
            child = Node(board,self.color,self,self.cost + 1,board.opponent(self.color), 0, move, (-1,-1))
            result.append(child)
        return result

def avaliacao():
    
    return

def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])

