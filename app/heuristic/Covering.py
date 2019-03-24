from chess import Board, Color, Square, Move
from utils.State import State

class Covering:

  def __init__(self, board: Board):
    self.__cache = dict()

    self.enemy_king_color: Color = not board.turn
    enemy_king_square: Square = board.king(self.enemy_king_color)

    self.mating_squares: [int] = list(board.attacks(enemy_king_square))
    self.mating_squares.append(enemy_king_square)

  def score(self, state: State) -> int:
    if state.id not in self.__cache:
      self.__cache[state.id] = self.__score(state)

    return self.__cache[state.id]

  def __score(self, state: State) -> int:
    
    h = 0
    for mating_square in self.mating_squares:
      h -= len(state.board.attackers(not self.enemy_king_color, mating_square))
    
    return h

