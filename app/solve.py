from chess import Board, Move
from time import time

from utils.State import State
from typing import List

from queue import PriorityQueue

from heuristic.Covering import Covering as Heuristic
from utils.ZobristHasher import ZobristHasher

def solve(board: Board, moves: int, timeout: int):

  if moves <= 0:
    return None

  # Initialize data structures
  queue = PriorityQueue()
  solved = dict()

  # Initialize starting state
  hf = Heuristic(board, moves)
  start = State(board, moves, None, None, False, hf, ZobristHasher(moves))
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

      if neighbor.id in solved:
        continue

      queue.put_nowait(neighbor)
      
  return False
    
    


      


    