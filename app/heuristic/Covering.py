from chess import Board, Color, Square, Move, PAWN, SQUARES 
from utils.State import State

class Covering:

  def __init__(self, board: Board, total_moves: int):
    self.__cache = dict()

    self.enemy_king_color: Color = not board.turn
    enemy_king_square: Square = board.king(self.enemy_king_color)

    self.mating_squares: [int] = list(board.attacks(enemy_king_square))
    self.mating_squares.append(enemy_king_square)

    self.total_moves = total_moves
    self.weight = 4.5/total_moves

  def score(self, state: State) -> int:
    if state.id not in self.__cache:
      self.__cache[state.id] = self.__score(state)

    return self.__cache[state.id]

  def __score(self, state: State) -> int:
    
    h = 0
    for mating_square in self.mating_squares:
      h -= len(state.board.attackers(not self.enemy_king_color, mating_square))
    
    return h + self.__promotion(state) + ((self.total_moves - state.moves_left) * self.weight) 

  def __promotion(self, state: State) -> int:
    
    step = 8
    stop = 64
    if not state.board.turn:
      step = -8
      stop = -1

    h = 0
    for pawn in state.board.pieces(PAWN, state.board.turn):
      from_square = pawn

      # Pawn path
      path = list(range(pawn+step, stop, step))
      path_len = len(path)

      # Is path short enough
      if path_len > state.moves_left:
        continue

      # Is path clear & not move in check
      is_possible = True
      for to_square in path:
        if state.board.piece_at(to_square):
          is_possible = False
          break
        if state.board.is_into_check(Move(from_square, to_square)):
          is_possible = False
          break
        from_square = to_square
      if not is_possible:
        continue

      h -= state.moves_left-path_len
    
    return h
      

  def __pin(self, state: State) -> int:
    return 0

