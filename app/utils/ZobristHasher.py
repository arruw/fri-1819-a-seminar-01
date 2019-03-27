import chess, random

class ZobristHasher:
  def __init__(self, total_moves: int):
    self.__table = [[random.randint(1,2**64 - 1) for fi in range(12)] for bi in range(64)]
    self.__moves = [random.randint(1,2**64 - 1) for mi in range(total_moves+1)]

  def hash(self, board: chess.Board, moves_left: int):
    zobrist_hash = 0

    zobrist_hash ^= self.__moves[moves_left]

    for squares in board.occupied_co:
      for square in chess.scan_reversed(squares):
        piece: chess.Piece = board.piece_at(square)
        piece_index = piece.piece_type
        if piece.color:
          piece_index *= 2
        zobrist_hash ^= self.__table[square][piece_index-1]

    return zobrist_hash
  
  def update(self, zobrist_hash, board: chess.Board, move: chess.Move, moves_left: int):
    piece: chess.Piece = board.piece_at(move.from_square)
    piece_index = piece.piece_type
    if piece.color:
      piece_index *= 2

    # Undo
    zobrist_hash ^= self.__table[move.from_square][piece_index-1]
    zobrist_hash ^= self.__moves[moves_left+1]

    # Do
    zobrist_hash ^= self.__table[move.to_square][piece_index-1]
    zobrist_hash ^= self.__moves[moves_left]

    return zobrist_hash


