import os, chess, time, sys
from solve import solve
from utils.Profiler import Profiler

def parseInput(input):
  f = open(input, 'r')
  raw = f.read()
  
  moves = int(raw.split(' ')[-1])
  fen = ' '.join(raw.split(' ')[:-1]) + ' KQkq - 0 1'
  
  board = chess.Board()
  board.set_fen(fen)

  return (board, moves)

files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1], f))]
passed = 0

profiler = Profiler()

for index, file in enumerate(files):
  board, moves = parseInput(file)
  
  start = time.time()
  profiler.enable()
  path = solve(board, moves, 20)
  profiler.disable()
  end = time.time()

  mark = '[SUCCESS]' if path else '[FAIL]   ' 
  if path:
    passed += 1

  print(f'{index+1}/{len(files)} {mark} {int(start)}+{int(end-start)} {path}')

print(f'Done, passed {passed} out of {len(files)}.')
profiler.print()
  


