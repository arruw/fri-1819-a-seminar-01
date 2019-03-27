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
      self.id = zhf.update(self.parent.id, self.parent.board, self.move, self.moves_left)
    except AttributeError:
      self.id = zhf.hash(self.board, self.moves_left)

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
    if self.moves_left <= 0:
      return

    for move in self.board.legal_moves:
      
      moves_left = self.moves_left-1

      # Copy board
      board: Board = self.board.copy(stack=False)
      board.move_stack = self.board.move_stack.copy()
      board.push(move)

      is_check = board.is_check()
      if moves_left > 0 and is_check:
        continue

      is_checkmate = not any(board.generate_legal_moves()) if is_check else False
      if moves_left == 0 and not is_checkmate:
        continue

      board.push(MOVE_NULL)

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
  