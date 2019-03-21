from chess import Board, Color, Square, square_distance, PIECE_TYPES
from utils.State import State
from functools import lru_cache

class Euclidean:

  def score(self, state: State) -> int:
    return self.__score(state)

  @lru_cache(maxsize=None)
  def __score(self, state: State) -> int:

    enemy_king_square: Square = state.board.king(not state.board.turn)

    """
    7 - max euclidean distance
    16 - max number of figures
    112 = 7 * 16
    """
    h = 112 
    for piece_type in PIECE_TYPES:
      for piece_square in state.board.pieces(piece_type, state.board.turn):
        h -= square_distance(piece_square, enemy_king_square)
    
    return h

