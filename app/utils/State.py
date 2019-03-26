from chess import Board, Move, SQUARE_NAMES, KING

MOVE_NULL = Move.null()

class State:

  def __init__(self, board: Board, moves_left: int, parent: 'State', move: Move, is_checkmate: bool, hf, zhf):
    # Core
    self.board = board
    self.moves_left = moves_left
    self.is_checkmate = is_checkmate

    # Pointer
    self.parent = parent
    self.move = move

    # Id
    self.zhf = zhf
    try:
      self.id = zhf.update(self.parent.id, self.parent.board, self.move)
    except AttributeError:
      self.id = zhf.hash(self.board)

    # Score
    self.hf = hf
    self.score = hf.score(self)

  def __hash__(self) -> int:
    return self.id

  def __eq__(self, other: 'State') -> bool:
    return other != None and self.id == other.id

  def __lt__(self, other: 'State') -> bool:
    return self.score < other.score
  
  def generate(self):
    if self.moves_left < 0:
      return

    for move in self.board.legal_moves:

      # Can't eat enemy king
      if self.board.piece_type_at(move.to_square) == KING:
        continue

      # Check is allowed only in last move
      if self.moves_left > 1 and self.board.is_into_check(move):
        continue
      
      # King can't move into check
      if self.board.piece_type_at(move.from_square) == KING and self.board.is_into_check(move):
        continue

      # Copy board
      board: Board = self.board.copy(stack=False)
      board.move_stack = self.board.move_stack.copy()

      # Make move
      board.push(move)
      is_checkmate = board.is_checkmate()
      moves_left = self.moves_left-1
      board.push(MOVE_NULL)

      if not is_checkmate and moves_left == 0:
        continue

      yield State(
        board=board,
        moves_left=moves_left,
        parent=self,
        move=move,
        is_checkmate=is_checkmate,
        hf=self.hf,
        zhf=self.zhf
      )

  def is_goal(self):
    return self.is_checkmate
    
  def get_path(self):
    uci = self.move.uci()
    path = uci[:2] + "-" + uci[2:]
    parent = self.parent
    while parent != None and parent.move != None:
      uci = parent.move.uci()
      path = uci[:2] + "-" + uci[2:] + ";" + path
      parent = parent.parent

    return path
  