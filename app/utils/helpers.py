import chess

def createBoardFromFen(input):
  f = open(input, 'r')
  raw = f.read()
  
  rounds = int(raw.split(' ')[-1])
  fen = ' '.join(raw.split(' ')[:-1]) + ' KQkq - 0 1'
  
  board = chess.Board()
  board.set_fen(fen)
    
  return (board, rounds)

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