import chess
import functools

class Covering:

  @functools.lru_cache(maxsize=None)
  def get(self, fen: str, moveUci: str) -> int:
    board = chess.Board(fen)
    
    enemy_king_color: chess.Color = not board.turn
    enemy_king_square: chess.Square = board.king(enemy_king_color)

    mating_squares: [int] = list(board.attacks(enemy_king_square))
    mating_squares.append(enemy_king_square)

    board.push(board.parse_uci(moveUci))

    h = 0
    for mating_square in mating_squares:
      h += len(board.attackers(not enemy_king_color, mating_square))
    
    return h


