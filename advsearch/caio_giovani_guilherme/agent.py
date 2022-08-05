from asyncio.windows_events import NULL
from curses.ascii import NUL
import random
import sys
from board import *
#from advsearch.othello import Board
#from othello.board import Board
import copy
MENOS_INFINITO = -1000
MAIS_INFINITO = 1000
WHITE = 'W'
BLACK = 'B'
# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

class Node:
    def __init__(self, board, p_color, parent=None,cost=1,color = WHITE, evaluation = 1,previous_move = (-1,-1), best_move = (-1,-1)):
        self.board = Board()
        self.player_color = p_color  
        self.parent = parent
        self.cost = cost
        self.color = color 
        self.eval = evaluation 
        self.previous_move = previous_move  
        self.best_move = best_move

    def node_print_board(self):
        print("Board: ")
        print(Board.print_board(self.board))

    
    def expande(self):
        result = []
        
        moves = self.board.legal_moves(self.color)
        for move in moves:
            board = copy.deepcopy(self.board)
            board.process_move(move,self.color)
            child = Node(board,self.color,self,self.cost + 1,board.opponent(self.color), 0, move, (-1,-1))
            result.append(child)
            child.node_print_board()
        
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
   
    
    return jogar(the_board,color)






def jogar(s,color):
    
    #to do, não sei como calcular o custo
    v = max_value(s,color,MENOS_INFINITO,MAIS_INFINITO)
    print(v)
    exit(7)
    return v

def utilidade(s: Board,color):
    board_state = str(s)
    utility = 0
    for c in board_state:
        if c == color:
            utility += 1
    return utility

def max_value(s: Board,color,alfa,beta):
    if s.is_terminal_state():
        return utilidade(s,color)
    
    v = MENOS_INFINITO
    
    for s1 in sucessores(s,color):
        v = max(v,min_value(s1,color,alfa,beta))
        
        alfa = max(alfa,v)
        if (alfa>=beta) :
            break
    return v

def min_value(s:Board,color,alfa,beta):
    if s.is_terminal_state():
        return utilidade(s,color)
    
    v = MAIS_INFINITO
    
    succ_list = sucessores(s,color)
    for s1 in succ_list:
        v = min(v,max_value(s1,color,alfa,beta))
        
        beta = min(beta,v)
        if (beta<=alfa) :
            break
    return v

    
def sucessores(s: Board, color): 
    filhos = []
    moves = s.legal_moves(color)
    for move in moves:
        board = copy.deepcopy(s)
        board.process_move(move,color)
        filhos.append(board)
    return filhos



