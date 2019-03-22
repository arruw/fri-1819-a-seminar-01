#!/usr/bin/env python3

from sys import argv
from chess import Board

from solve import solve
from utils.Profiler import Profiler

def main(argv):
  assert len(argv) >= 2

  input = argv[1]
  timeout = 20
  profile = True

  f = open(input, 'r')
  raw = f.read()
  
  moves = int(raw.split(' ')[-1])
  fen = ' '.join(raw.split(' ')[:-1]) + ' KQkq - 0 1'
  
  board = Board()
  board.set_fen(fen)
    
  profiler = None
  if profile:
    profiler = Profiler()
    profiler.enable()

  path = solve(board, moves, timeout)

  if profile:
    profiler.disable()
    profiler.print()

  print(path)

if __name__ == '__main__':
  main(argv)
