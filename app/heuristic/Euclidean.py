from chess import Square, square_distance, PIECE_TYPES
from utils.State import State

class Euclidean:

  def __init__(self):
    self.__cache = dict()

  def score(self, state: State) -> int:
    if state.id in self.__cache:
      return self.__cache[state.id]

    h = self.__score(state)
    self.__cache[state.id] = h

    return h

  def __score(self, state: State) -> int:

    enemy_king_square: Square = state.board.king(not state.board.turn)

    h = 0 
    for piece_type in PIECE_TYPES:
      for piece_square in state.board.pieces(piece_type, state.board.turn):
        h -= square_distance(piece_square, enemy_king_square)
    
    return h

