import cProfile, pstats, io

class Profiler:
  def __init__(self):
    self.__profile = cProfile.Profile(builtins=False)

  def enable(self):
    self.__profile.enable(builtins=False)

  def disable(self):
    self.__profile.disable()

  def print(self):
    s = io.StringIO()
    ps = pstats.Stats(self.__profile, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())