#!/usr/bin/env python3

import sys, random, queue, chess

# Prevents initializing NULL move many times
MOVE_NULL = chess.Move.null()

class State:

  """
  Defines tree structure for A* algorithm.

  - generate => Function generates siblings
  - is_goal => Function check if current state is goal
  - get_path => Function constructs solution path

  """

  def __init__(self, board, movesLeft, parent, move, is_checkmate, hf, zhf):
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

  def __hash__(self):
    return self.id

  def __eq__(self, other):
    return other != None and self.id == other.id

  def __lt__(self, other):
    return self.score < other.score
  
  def generate(self):
    if self.movesLeft <= 0:
      return

    def __next(move):
      board = self.board.copy(stack=False)
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
      if self.board.piece_type_at(move.to_square) == chess.KING:
        continue

      # Check is allowed only in last move
      if self.movesLeft > 1 and self.board.is_into_check(move):
        continue
      
      # King can't move into check
      if self.board.piece_type_at(move.from_square) == chess.KING and self.board.is_into_check(move):
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


class Covering:

  """
  Defines Covering Heuristics for A* algorithm.

  Covering Heuristics count how many times enemy mating squares are attacked by us.
  + Promotions
  + Pins
  """

  def __init__(self, board):
    self.__cache = dict()

    self.enemy_king_color = not board.turn
    enemy_king_square = board.king(self.enemy_king_color)

    self.mating_squares = list(board.attacks(enemy_king_square))
    self.mating_squares.append(enemy_king_square)

  def score(self, state):
    if state.id not in self.__cache:
      self.__cache[state.id] = self.__score(state)

    return self.__cache[state.id]

  def __score(self, state):
    
    h = 0
    for mating_square in self.mating_squares:
      h -= len(state.board.attackers(not self.enemy_king_color, mating_square))
    
    return h + self.__promotion(state)

  def __promotion(self, state):
    
    """
    Count number of pawns that can promote.

    Pawn can promote if:
    - number of moves to promotion must be achievable in number of moves that are left
    - file path to promotion is clear
    - pawn can not move into check
    """

    step = 8
    stop = 64
    if not state.board.turn:
      step = -8
      stop = -1

    h = 0
    for pawn in state.board.pieces(chess.PAWN, state.board.turn):
      from_square = pawn

      # Pawn path
      path = list(range(pawn+step, stop, step))
      path_len = len(path)

      # Is path short enough
      if path_len > state.movesLeft:
        continue

      # Is path clear & not move in check
      is_possible = True
      for to_square in path:
        if state.board.piece_at(to_square):
          is_possible = False
          break
        if state.board.is_into_check(chess.Move(from_square, to_square)):
          is_possible = False
          break
        from_square = to_square
      if not is_possible:
        continue

      h -= 1
    
    return h
      
  def __pin(self, state):
    return 0


class ZobristHasher:

  """
  Defines Zobrist hash for 8*8 chess board.

  This is used to quickly calculate hash value of board.

  - hash => Function calculate initial hash value (this should be called only once)
  - update => Function update previously calculated hash value with the given move
  """

  def __init__(self):
    self.__table = [[random.randint(1,2**64 - 1) for fi in range(12)] for bi in range(64)]

  def hash(self, board):
    zobrist_hash = 0

    for squares in board.occupied_co:
      for square in chess.scan_reversed(squares):
        piece = board.piece_at(square)
        piece_index = piece.piece_type
        if piece.color:
          piece_index *= 2
        zobrist_hash ^= self.__table[square][piece_index-1]

    return zobrist_hash
  
  def update(self, zobrist_hash, board, move):
    if not move:
      return zobrist_hash

    piece = board.piece_at(move.from_square)
    piece_index = piece.piece_type
    if piece.color:
      piece_index *= 2

    zobrist_hash ^= self.__table[move.from_square][piece_index-1]
    zobrist_hash ^= self.__table[move.to_square][piece_index-1]

    return zobrist_hash


def solve(board, moves):

  """
  This method implements A* algorithm.
  """

  if moves <= 0:
    return None

  # Initialize data structures
  generated = queue.PriorityQueue()
  solved = dict()

  # Initialize starting state
  hf = Covering(board)
  start = State(board, moves, None, None, False, hf, ZobristHasher())
  generated.put_nowait(start)

  while not generated.empty():
    current = generated.get_nowait()
    solved[current.id] = current

    # We found solution 
    if current.is_goal():
      return current.get_path()

    # We can not do more moves
    if current.movesLeft == 0:
      continue

    # Generate possible next states
    for neighbor in current.generate():
      
      if neighbor.id in solved:
        if solved[neighbor.id].movesLeft > neighbor.movesLeft:
          continue
        else:
          del solved[neighbor.id]

      generated.put_nowait(neighbor)
      
  return False
    

input = sys.argv[1]
f = open(input, 'r')
raw = f.read()
  
moves = int(raw.split(' ')[-1])
fen = ' '.join(raw.split(' ')[:-1]) + ' KQkq - 0 1'
  
board = chess.Board()
board.set_fen(fen)
    
path = solve(board, moves)

print(path)