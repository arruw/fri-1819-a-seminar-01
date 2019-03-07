from queue import PriorityQueue

class PriorityHashQueue:

  def __init__(self):
    self.__pq = PriorityQueue()
    self.__hl = {}

  def empty(self) -> bool:
    return self.__pq.empty()

  def push(self, item):
    self.__pq.put_nowait(item)
    self.__hl[item.id] = item

  def pop(self):
    top = self.__pq.get_nowait()
    del self.__hl[top.id]
    return top

  def get(self, id: str):
    return self.__hl[id]

  def has(self, id: str) -> bool:
      return id in self.__hl