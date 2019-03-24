from chess import Board, Square, square_distance, PIECE_TYPES
from utils.State import State

class Euclidean:

  def __init__(self, board: Board):
    self.__cache = dict()
    self.enemy_king_square: Square = board.king(not board.turn)

  def score(self, state: State) -> int:
    if state.id not in self.__cache:
      self.__cache[state.id] = self.__score(state)

    return self.__cache[state.id]

  def __score(self, state: State) -> int:

    h = 0 
    for piece_type in PIECE_TYPES:
      for piece_square in state.board.pieces(piece_type, state.board.turn):
        h -= square_distance(piece_square, self.enemy_king_square)
    
    return h

