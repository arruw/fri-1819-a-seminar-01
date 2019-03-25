from chess import Board, Move, SQUARE_NAMES, KING

MOVE_NULL = Move.null()

class State:

  def __init__(self, board: Board, movesLeft: int, parent: 'State', move: Move, is_checkmate: bool, hf, zhf):
    # Core
    self.board = board
    self.movesLeft = movesLeft
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
    if self.movesLeft <= 0:
      return

    def __next(move: Move) -> 'State':
      board: Board = self.board.copy(stack=False)
      board.move_stack = self.board.move_stack.copy()
      board.push(move)
      is_checkmate = board.is_checkmate()
      board.push(MOVE_NULL)

      return State(
        board=board,
        movesLeft=self.movesLeft-1,
        parent=self,
        move=move,
        is_checkmate=is_checkmate,
        hf=self.hf,
        zhf=self.zhf
      )

    for move in self.board.legal_moves:

      # Can't eat enemy king
      if self.board.piece_type_at(move.to_square) == KING:
        continue

      # Check is allowed only in last move
      if self.movesLeft > 1 and self.board.is_into_check(move):
        continue
      
      # King can't move into check
      if self.board.piece_type_at(move.from_square) == KING and self.board.is_into_check(move):
        continue

      yield __next(move)

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
  