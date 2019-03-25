import chess, random

class ZobristHasher:
  def __init__(self):
    self.__table = [[random.randint(1,2**64 - 1) for fi in range(12)] for bi in range(64)]

  def hash(self, board: chess.Board):
    zobrist_hash = 0

    for squares in board.occupied_co:
      for square in chess.scan_reversed(squares):
        piece: chess.Piece = board.piece_at(square)
        piece_index = piece.piece_type
        if piece.color:
          piece_index *= 2
        zobrist_hash ^= self.__table[square][piece_index-1]

    return zobrist_hash
  
  def update(self, zobrist_hash, board: chess.Board, move: chess.Move):
    if not move:
      return zobrist_hash

    piece: chess.Piece = board.piece_at(move.from_square)
    piece_index = piece.piece_type
    if piece.color:
      piece_index *= 2

    zobrist_hash ^= self.__table[move.from_square][piece_index-1]
    zobrist_hash ^= self.__table[move.to_square][piece_index-1]

    return zobrist_hash


