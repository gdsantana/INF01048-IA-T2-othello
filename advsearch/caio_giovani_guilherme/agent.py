from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY, NULL
from cmath import inf
from curses.ascii import NUL
import random
from shutil import move
import sys
import numpy
import operator
from board import *
import time
#from advsearch.othello import Board
#from othello.board import Board
from ..othello import board
import copy
MENOS_INFINITO = -1000
MAIS_INFINITO = 1000
WHITE = 'W'
BLACK = 'B'
TEMPO_LIMITE = 5
# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

position_weights = numpy.matrix([
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
])

class Node:
  
    def __init__(self, board, move, color, cost = 0, children=[], t0 = 0):
        self.board = board
        self.move = move
        self.color = color
        self.cost = cost
        self.children = children
        self.t0 = t0


    def children_value(self,v):
        for chil in self.children:
            #print("valor de v:" + str(v))
            #print("valor de chil cost:" + str(chil.cost))

            if chil.cost == v:
                #print("entrou aqui")
                return chil

        return None


    def node_print_board(self):
        print("Board: ")
        print(Board.print_board(self.board))

    
    def expande(self):
        result = []
        
        moves = self.board.legal_moves(self.color)
       
    
        for move in moves:
            
            board1 = copy.deepcopy(self.board)
            board1.process_move(move, self.color)
            child = Node(board1, move, self.board.opponent(self.color),cost=self.cost+1,t0 = time.time())
            self.children.append(child)
            result.append(child)
       
        
        return result

def get_points(board: board.Board) -> tuple[int, int]:
    """
    Returns a tuple (a,b) where a is the agent's points, and b is the opponent's points
    """
    p1_score = sum([1 for char in str(board) if char == COLOR_AG])
    p2_score = sum([1 for char in str(board) if char == COLOR_OP])

    return (p1_score, p2_score)

   
def coin_difference(board: board.Board):
    """
    Coin Difference:
        A heurística Coin Difference simplesmente avalia a atual posição do tabuleiro e calcula a diferença de pontos entre os 	jogadores.
        100 * (PlayerPoints - OponentPoints) / (PlayerPoints + OponentPoints)
    """
    player_points, opponent_points = get_points(board)

    if player_points + opponent_points == 0:
        return 0
    return 100 * (player_points - opponent_points)/(player_points + opponent_points)

def potential_mobility(board: board.Board):
    directions = [(1,-1),(1,0),(1,1),(0,-1),(0,0),(0,1),(-1,-1),(-1,0),(-1,1)]
    ag_surrounding = 0
    op_surrounding = 0
    for i in range(8):
        for j in range(8):        
            if (board.tiles[i][j] != '.'):
                for a, b in directions:
                    x = i + a
                    y = j + b
                    if x >= 0 and x < 8 and y >=0 and y < 8 and board.tiles[x][y] == '.':
                        if board.tiles[i][j] == COLOR_AG:
                            ag_surrounding += 1
                        else:
                            op_surrounding += 1
    if ag_surrounding != 0 or op_surrounding != 0:
        return 100*(ag_surrounding-op_surrounding)/(ag_surrounding+op_surrounding)
    else:
        return 0


def base_mobility(board: board.Board) -> int:
    #print(len(board.legal_moves(COLOR_AG)))
    #print(len(board.legal_moves(COLOR_OP)))
    if (len(board.legal_moves(COLOR_AG)) + len(board.legal_moves(COLOR_OP))) > 0:
        return (100*(len(board.legal_moves(COLOR_AG))-len(board.legal_moves(COLOR_OP)))/(len(board.legal_moves(COLOR_AG)) + len(board.legal_moves(COLOR_OP))))
    else:
        return 0

def close_to_corners(board: board.Board):
    close_ag = 0
    close_op = 0

    corners = [(0,0),(0,7),(7,0),(7,7)]
    close_to_corners = [(0,1),(1,0),(0,6),(1,7),(1,6),(6,0),(7,1),(6,1),(6,7),(7,6),(6,6)]

    for i, j in corners:
        if board.tiles[i][j] != '.':
            for a, b in close_to_corners:
                if board.tiles[a][b] == COLOR_AG:
                    close_ag += 1
                elif board.tiles[a][b] == COLOR_OP:
                    close_op += 1

    return close_op-close_ag

def corners_captured(board: board.Board):
    corners = [(0,0),(0,7),(7,0),(7,7)]
    corners_ag = 0
    corners_op = 0

    for a, b in corners:
        if board.tiles[a][b] == COLOR_AG:
            corners_ag += 1
        elif board.tiles[a][b] == COLOR_OP:
            corners_op += 1

    if corners_op + corners_ag != 0:
        return 100 * (corners_ag - corners_op) / (corners_ag + corners_op)
    else:
        return 0

def move_sort(move):
    return -position_weights[move[1], move[0]]

def move_priority(agent: board.Board) -> list[tuple[int, int]]:
    moves = agent.legal_moves(COLOR_AG)
    
    moves.sort(key=move_sort)
    print(moves)
    return moves


'''def avaliacao(s: Node):
    board = s.board
    color = s.color

    number_of_pieces=board.piece_count[color] 
    number_of_moves=len(board.legal_moves(color)) 
    corners=[board.tiles[0][0],board.tiles[0][7],board.tiles[7][0],board.tiles[7][7]] 
    if board.EMPTY in corners: 
        return number_of_pieces + 4 * number_of_moves + 20 * corners.count(color)-20*corners.count(board.opponent(color)) 
    return 5 * number_of_pieces + 2 * number_of_moves + 20 * corners.count(color)-20*corners.count(board.opponent(color))'''

def heuristics(s: Node) -> int:
    points = get_points(BOARD)
    total = points[0] + points[1]


    if total <=10:
        return 10000
    elif total <= 25:
        #print(BOARD)
        #print("Begin")
        #print(corners_captured(BOARD))
        #print(base_mobility(BOARD))
        #print(potential_mobility(BOARD))
        #print(close_to_corners(BOARD))
        return 5*corners_captured(BOARD) + 25*base_mobility(BOARD) + 25*potential_mobility(BOARD) #+ 15*close_to_corners(BOARD)
    elif total <= 50:
        return 30*corners_captured(BOARD) + 20*base_mobility(BOARD) + 20*potential_mobility(BOARD) + 25*coin_difference(BOARD) #+ 15*close_to_corners(BOARD)
    else:
        return 30*corners_captured(BOARD) + 15*base_mobility(BOARD) + 15*potential_mobility(BOARD) + 25*coin_difference(BOARD) #+ 10*close_to_corners(BOARD)

def avaliacao(s : Node): #quantas peças daquela cor
    board = str(s.board)
    color = s.color
    value = 0
    for c in board:
        if c == color:
            value += 1
    return value    
    

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
    global COLOR_AG, COLOR_OP, BOARD
    COLOR_AG = color
    if COLOR_AG == 'B':
        COLOR_OP = 'W'
    else:
        COLOR_OP = 'B'
    BOARD = the_board

    moves_available = move_priority(the_board)
    if len(moves_available) == 0:
        return (-1,-1)
    else:
        node = Node(the_board,None,color,t0 = time.time())
        ok = jogar(node)
        if ok in moves_available:
            return ok
        else:
            return moves_available[0]



def jogar(s: Node):
    
    #to do, não sei como calcular o custo
    
    v = max_value(s,MENOS_INFINITO,MAIS_INFINITO)
    children_with_that_value: Node = s.children_value(v)
    if children_with_that_value == None:
        return(-1,-1)
    else:
        return children_with_that_value.move

def utilidade(s: Node):
    u = heuristics(s)
    #u = avaliacao(s)
    #u = get_coin_difference(s.board,s.color)
    return u

def max_value(s: Node,alfa,beta):
    tf = time.time()
    if s.board.is_terminal_state() or (tf - s.t0) > TEMPO_LIMITE:
        u = heuristics(s)
        #print(u)
        s.cost = u
        return u
    
    v = MENOS_INFINITO
    

    for s1 in s.expande():
        v = max(v,min_value(s1,alfa,beta))
        
        alfa = max(alfa,v)
        if (alfa>=beta) :
            break
    s.cost = v
    return v

def min_value(s: Node,alfa,beta):
    tf = time.time()
    if s.board.is_terminal_state() or (tf - s.t0) > TEMPO_LIMITE:
        u = heuristics(s)
        #print(u)
        s.cost = u
        return u
    
    v = MAIS_INFINITO
    
    succ_list = s.expande()
    for s1 in succ_list:
        v = min(v,max_value(s1,alfa,beta))
        
        beta = min(beta,v)
        if (beta>=alfa) :
            break
    s.cost = v
    return v




