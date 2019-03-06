import chess

import utils.helpers as helpers

from datastructures.Node import Node
from datastructures.PriorityQueue import PriorityQueue
from heuristic.Covering import Covering as Heuristic

def solve(input):
  pq = PriorityQueue()
  h = Heuristic()
  (board, rounds) = helpers.createBoardFromFen(input)
  print(board)