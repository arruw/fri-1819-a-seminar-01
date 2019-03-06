import chess

class Node:
  def __init__(self, board: chess.Board, rounds: int, mark: int):
    self.board = board
    self.rounds = rounds
    self.mark = mark

  def __gt__(self, other) -> bool:
    return self.mark > other.mark
    
  def key(self) -> str:
    return f'{self.board.fen()} {self.rounds}'