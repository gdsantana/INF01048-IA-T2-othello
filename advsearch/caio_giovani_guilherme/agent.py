


global COLOR_AG, COLOR_OP, BOARD

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

TEMPO_LIMITE = 4.9
# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.
succ_list = []
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


def get_points(board: Board) -> tuple[int, int]:
    """
    Returns a tuple (a,b) where a is the agent's points, and b is the opponent's points
    """
  
    p1_score = sum([1 for char in str(board) if char == COLOR_AG])
    p2_score = sum([1 for char in str(board) if char == COLOR_OP])

    return (p1_score, p2_score)

   
def coin_difference(board: Board):
    """
    Coin Difference:
        A heurística Coin Difference simplesmente avalia a atual posição do tabuleiro e calcula a diferença de pontos entre os 	jogadores.
        100 * (PlayerPoints - OponentPoints) / (PlayerPoints + OponentPoints)
    """
    player_points, opponent_points = get_points(board)

    if player_points + opponent_points == 0:
        return 0
    return 100 * (player_points - opponent_points)/(player_points + opponent_points)

def potential_mobility(board: Board):
   
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


def base_mobility(board: Board) -> int:
    
    if (len(board.legal_moves(COLOR_AG)) + len(board.legal_moves(COLOR_OP))) > 0:
        return (100*(len(board.legal_moves(COLOR_AG))-len(board.legal_moves(COLOR_OP)))/(len(board.legal_moves(COLOR_AG)) + len(board.legal_moves(COLOR_OP))))
    else:
        return 0

def close_to_corners(board: Board):
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

def corners_captured(board: Board):
    
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

def move_priority(agent: Board) -> list[tuple[int, int]]:
    
    moves = agent.legal_moves(COLOR_AG)
    
    moves.sort(key=move_sort)
    print(moves)
    return moves



def heuristics(s: Board) -> int:
    BOARD = s
    points = get_points(BOARD)
    total = points[0] + points[1]


    if total <= 25:
        return 5*corners_captured(BOARD) + 25*base_mobility(BOARD) + 25*potential_mobility(BOARD) + 15*close_to_corners(BOARD)
    elif total <= 50:
        return 30*corners_captured(BOARD) + 20*base_mobility(BOARD) + 20*potential_mobility(BOARD) + 25*coin_difference(BOARD) + 15*close_to_corners(BOARD)
    else:
        return 30*corners_captured(BOARD) + 15*base_mobility(BOARD) + 15*potential_mobility(BOARD) + 25*coin_difference(BOARD) + 10*close_to_corners(BOARD)





def successors(state: Board, color):
    succlist = []
    legal_moves = state.legal_moves(color)
    for move in legal_moves:
        strs = from_string(str(state))
        strs.process_move(move, color)
        succlist.append(strs)
    return succlist


def max_value(s: Board,alfa,beta,t0,color):
    v = -inf
    sucessores = successors(s,color)
    tf = time.time()
    if sucessores==NULL or s.is_terminal_state() or (tf - t0) < TEMPO_LIMITE:
        u = heuristics(s)
        v = u
        return v
    

    ###if  (tf - t0) < TEMPO_LIMITE:
    ###    print("tf - t0" + str(tf-t0))
    ##    return heuristics(s)
    for son in sucessores:
        v = max(v, min_value(son, alfa, beta, t0, color))
        alfa = max(alfa, v)
        if alfa >= beta: break
        
    return v
    
    


def min_value(s: str,alfa,beta,t0,color):
    v=inf
    sucessores = successors(s,color)
    tf = time.time()
    if sucessores==NULL or s.is_terminal_state() or (tf - t0) < TEMPO_LIMITE: 
        u = heuristics(s)
        v = u
        return v
    
    
    for son in sucessores:
        v = min(v, max_value(son, alfa, beta, t0, color))
        beta = min(beta, v)
        if beta <= alfa: break
        
    return v






def jogar(state : Board, t0, color): 
    melhor_suc = 0
    
    succ_list = successors(state, color)
    if not succ_list:
        return (-1,-1)
    

    legal_moves =state.legal_moves(color)
    moves = list(zip(succ_list,legal_moves))
    i = 0 
    melhor_suc = max(succ_list, key= lambda s: min_value(s, -inf, inf, t0, color))
    index = 0
    for move in moves:
        
        #print("move[0] = " + str(move[0]))
        #print("melhor_suc = " + str(melhor_suc))
        if move[0] == melhor_suc:
            print("entro aq" + str(move[1]))
            index = i
        i = i+1
    #print("moves[index]:" + str(moves[index]))
    return moves[index][1]
    
def make_move(the_board : Board, color):
	
    global COLOR_AG, COLOR_OP
    COLOR_AG = color
    if COLOR_AG == 'B':
        COLOR_OP = 'W'
    else:
        COLOR_OP = 'B'
    color = COLOR_AG
    #the_board.process_move(move, color)
    move = jogar(the_board, time.time(), color)
    
    
    if the_board.is_legal(move,color):
        the_board.process_move(move, color)
        return move
    else:
        legal_moves = the_board.legal_moves(color)
        return legal_moves[0] if len(legal_moves) > 0 else (-1, -1)







