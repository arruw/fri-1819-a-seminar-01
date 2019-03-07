from chess import Board, Color, Square
from functools import lru_cache

class Covering:

  @lru_cache(maxsize=None)
  def get(self, fen: str) -> int:
    
    board = Board(fen=fen)

    enemy_king_color: Color = not board.turn
    enemy_king_square: Square = board.king(enemy_king_color)

    mating_squares: [int] = list(board.attacks(enemy_king_square))
    mating_squares.append(enemy_king_square)

    h = 0
    for mating_square in mating_squares:
      h += len(board.attackers(not enemy_king_color, mating_square))
    
    return h


