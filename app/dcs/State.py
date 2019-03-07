from chess import Board
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class State:
  id: str=field(compare=False, hash=True)
  board: Board=field(compare=False, hash=False)
  rounds: int=field(compare=False, hash=False)
  g: int=field(compare=False, hash=False)
  f: int=field(compare=True, hash=False)