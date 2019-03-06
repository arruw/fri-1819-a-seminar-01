# Install dependencies
!pip install python-chess

# Import dependencies
import pandas as pd
import chess
import os

from google.colab import drive

# Mount Google Drive
drive.mount('/content/gdrive/')

import heapq

class PriorityQueue:
  def __init__(self):
    self.elements = []

  def empty(self):
    return len(self.elements) == 0

  def put(self, item, priority):
    heapq.heappush(self.elements, (priority, item))

  def get(self):
    return heapq.heappop(self.elements)[1]
  
class State:
  def __init__(self, board, rounds, mark):
    self.board = board
    self.rounds = rounds
    self.mark = mark
    
  def __gt__(self, other):
    return self.mark > other.mark
    
  def key(self):
    return f'{self.board.fen()} {self.rounds}'
  
  
  
def play(start, cost_f, heuristic_f):
    
  frontier = PriorityQueue()
  frontier.put(start, start.mark)
  came_from = {}
  cost_so_far = {}
  came_from[start.key()] = None
  cost_so_far[start.key()] = start.mark

  # Find enemy king position
  goal = list(start.board.pieces(chess.KING, not board.turn))[0]
  
  while not frontier.empty():
      current = frontier.get()

      #print('In loop...')
      
      if current.board.is_game_over():
        print('Game is over')
        break
      
      moves = generateMoves(current.board, current.rounds)
      
      #print(f'Possible moves: {len(moves)}')
      
      for move in moves:
          #print(move)
          next_board = current.board.copy(stack=False)
          next_board.push(move)
          next_board.push(chess.Move.null())
          move_from = chess.SQUARE_NAMES.index(move.uci()[:2])
          new_cost = cost_so_far[current.key()] + 1
          next = State(next_board, current.rounds - 1, new_cost)
          if next not in cost_so_far or new_cost < cost_so_far[next.key()]:
              cost_so_far[next.key()] = new_cost
              priority = new_cost + heuristic_f(move_from, goal)
              next.mark = priority
              frontier.put(next, priority)
              came_from[next.key()] = current
         
  return came_from, cost_so_far

# ============================
def createBoardForExample(id):
  f = open(f'/content/gdrive/My Drive/Fri/Fri 2018 2019/S02/A/Seminars/01/inputs/{id}.txt', 'r')
  raw = f.read()
  
  rounds = int(raw.split(' ')[-1])
  fen = ' '.join(raw.split(' ')[:-1]) + ' KQkq - 0 1'
  
  board = chess.Board()
  board.set_fen(fen)
    
  return (board, rounds)


# ============================
def generateMoves(board, rounds):
  
  if rounds == 0:
    return list()
  
  def notMoveIntoCheck(move):
    return not board.is_into_check(move)
  
  def notMoveKingIntoCheck(move):
    return not (board.piece_type_at(chess.SQUARE_NAMES.index(move.uci()[:2])) == chess.KING and
    board.is_into_check(move))
    
  moves = board.legal_moves

  if rounds > 1:
    moves = filter(notMoveIntoCheck, moves)
  else:
    moves = filter(notMoveKingIntoCheck, moves)
  
  return list(moves)


# ============================
def h_square_distance(a, b):
  return chess.square_distance(a, b)

(board, rounds) = createBoardForExample(1)