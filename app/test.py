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

  return (board, moves, raw)

files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1], f))]
passed = 0

profiler = Profiler()

for index, file in enumerate(sorted(files)):
  board, moves, fenx = parseInput(file)
  
  start = time.time()
  profiler.enable()
  path = solve(board, moves, 20)
  profiler.disable()
  end = time.time()

  mark = '[FAIL]   ' 
  if path:
    if len(path.split(';')) == moves:
      mark = '[SUCCESS]'
      passed += 1
    else:
      mark = '[ERROR]  '

  print(f'{index+1:02d}/{len(files)} {mark} {int(start)}+{int(end-start):02d} {file}\n\t{fenx}\n\t{path}')

print(f'Done, passed {passed} out of {len(files)}.')
profiler.print()
  


