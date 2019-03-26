from chess import Board, Move
from time import time

from utils.State import State
from typing import List

from queue import PriorityQueue

from heuristic.Covering import Covering as Heuristic
from utils.ZobristHasher import ZobristHasher

# TODO: https://www.growingwiththeweb.com/2012/06/a-pathfinding-algorithm.html
# http://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
# https://gitlab.com/dsaiko
# http://eprints.fri.uni-lj.si/3610/1/63100292-MITJA_RIZVI%C4%8C-Avtomatsko_odkrivanje_zanimivih_%C5%A1ahovskih_problemov.pdf
def solve(board: Board, moves: int, timeout: int):

  if moves <= 0:
    return None

  # Initialize data structures
  queue = PriorityQueue()
  solved = dict()

  # Initialize starting state
  hf = Heuristic(board)
  start = State(board, moves, None, None, False, hf, ZobristHasher())
  queue.put_nowait(start)

  time_limit = time() + timeout
  while not queue.empty() and time() < time_limit:
    current: State = queue.get_nowait()
    solved[current.id] = current

    # We found solution 
    if current.is_goal():
      return current.get_path()

    # Generate possible next states
    for neighbor in current.generate():

      try:
        if solved[neighbor.id].moves_left > neighbor.moves_left:
          continue
        else:
          del solved[neighbor.id]
      except KeyError:
        pass

      queue.put_nowait(neighbor)
      
  return False
    
    


      


    