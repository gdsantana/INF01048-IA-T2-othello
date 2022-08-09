from asyncio.windows_events import NULL
from curses.ascii import NUL
import random
import sys
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

def get_points(board: board.Board, agent_color: str) -> tuple[int, int]:
    """
    Returns a tuple (a,b) where a is the agent's points, and b is the opponent's points
    """
    oponent_color = board.opponent(agent_color)
    p1_score = sum([1 for char in str(board) if char == agent_color])
    p2_score = sum([1 for char in str(board) if char == oponent_color])

    return (p1_score, p2_score)

   
def get_coin_difference(board: board.Board, agent_color: str):
    """
    Coin Difference:
        A heurística Coin Difference simplesmente avalia a atual posição do tabuleiro e calcula a diferença de pontos entre os 	jogadores.
        100 * (PlayerPoints - OponentPoints) / (PlayerPoints + OponentPoints)
    """
    player_points, opponent_points = get_points(board, agent_color)

    if player_points + opponent_points == 0:
        return 0
    return 100 * (player_points - opponent_points)/(player_points + opponent_points)


'''def avaliacao(s: Node):
    board = s.board
    color = s.color

    number_of_pieces=board.piece_count[color] 
    number_of_moves=len(board.legal_moves(color)) 
    corners=[board.tiles[0][0],board.tiles[0][7],board.tiles[7][0],board.tiles[7][7]] 
    if board.EMPTY in corners: 
        return number_of_pieces + 4 * number_of_moves + 20 * corners.count(color)-20*corners.count(board.opponent(color)) 
    return 5 * number_of_pieces + 2 * number_of_moves + 20 * corners.count(color)-20*corners.count(board.opponent(color))'''

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
   
    
    node = Node(the_board,None,color,t0 = time.time())
    # return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])
    
    return jogar(node)






def jogar(s: Node):
    
    #to do, não sei como calcular o custo
    
    v = max_value(s,MENOS_INFINITO,MAIS_INFINITO)
    children_with_that_value: Node = s.children_value(v)
    if children_with_that_value == None:
        return(-1,-1)
    else:
        return children_with_that_value.move

def utilidade(s: Node):
    #u = avaliacao(s)
    u = get_coin_difference(s.board,s.color)
    return u

def max_value(s: Node,alfa,beta):
    tf = time.time()
    if s.board.is_terminal_state() or (tf - s.t0) > TEMPO_LIMITE:
        u = utilidade(s)
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
        u = utilidade(s)
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




