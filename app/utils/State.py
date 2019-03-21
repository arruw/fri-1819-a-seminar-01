from chess import Board, Move, SQUARE_NAMES, KING

class State:

  def __init__(self, board: Board, movesLeft: int, parent: 'State', move: str, hf, zhf):
    # Core
    self.board = board
    self.movesLeft = movesLeft

    # Pointer
    self.parent = parent
    self.move = move

    # Id
    # self.fen = board.fen()
    # self.id = hash(self.fen + str(movesLeft))
    self.zhf = zhf
    self.id = zhf.update(self.parent.id, self.parent.board, Move.from_uci(self.move)) if self.parent != None else zhf.hash(self.board)

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
      board = self.board.copy()
      board.push(move)
      board.push(Move.null())

      return State(
        board=board,
        movesLeft=self.movesLeft-1,
        parent=self,
        move=move.uci(),
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
    self.board.push(Move.null())
    is_checkmate = self.board.is_checkmate()
    self.board.pop()
    return is_checkmate
    
  def get_path(self):
    path = self.move[:2] + "-" + self.move[2:]
    parent = self.parent
    while parent != None and parent.move != None:
      path = parent.move[:2] + "-" + parent.move[2:] + ";" + path
      parent = parent.parent

    return path
  