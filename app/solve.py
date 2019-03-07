from chess import Board, Move

from datastructures.PriorityHashQueue import PriorityHashQueue
from dcs.State import State
from typing import List

import utils.helpers as helpers

from heuristic.Covering import Covering as Heuristic

import queue

# TODO: https://www.growingwiththeweb.com/2012/06/a-pathfinding-algorithm.html
# http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
def solve(input):
  (board, rounds) = helpers.createBoardFromFen(input)

  if rounds <= 0:
    return None

  hf = Heuristic()
  start_fen = board.fen()
  start = State(start_fen, board, rounds, 0, hf.get(start_fen))

  # Open
  pq = PriorityHashQueue()
  pq.push(start)

  # Closed
  c = {}
  
  # Path
  path = {}

  while not pq.empty():
    current: State = pq.pop()

    # We found solution 
    if current.board.is_game_over():
      break # TODO: construct path

    c[current.id] = current

    # We can not do more moves
    if current.rounds == 0:
      continue

    moves: List[Move] = helpers.generateMoves(board, current.rounds)
    for move in moves:
      next_board: Board = current.board.copy(stack=False)
      next_board.push(move)
      next_board.push(Move.null())
      next_id = next_board.fen()

      if next_id in c:
        print('next_id in c ... continue ...')
        continue
      
      next_g = current.g + 1 # TODO: + ?
      next_h = hf.get(next_id)
      next_f = next_g + next_h

      next = State(next_id, next_board, rounds-1, next_g, next_f)

      if not pq.has(next_id):
        pq.push(next)
      elif next_g >= c[next_id].g:
        continue   

      path[next_id] = current
      
  return path
    
    


      


    