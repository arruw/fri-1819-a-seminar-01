from chess import Board, Color, Square, Move
from utils.State import State
from functools import lru_cache

class Covering:

  def score(self, state: State) -> int:
    return self.__score(state)

  @lru_cache(maxsize=None)
  def __score(self, state: State) -> int:
    
    enemy_king_color: Color = not state.board.turn
    enemy_king_square: Square = state.board.king(enemy_king_color)

    mating_squares: [int] = list(state.board.attacks(enemy_king_square))
    mating_squares.append(enemy_king_square)

    h = 0
    for mating_square in mating_squares:
      h += len(state.board.attackers(not enemy_king_color, mating_square))
    
    return h

