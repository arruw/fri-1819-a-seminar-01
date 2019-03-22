import cProfile, pstats, io

class Profiler:
  def __init__(self):
    self.profile = cProfile.Profile(builtins=False)

  def enable(self):
    self.profile.enable(builtins=False)

  def disable(self):
    self.profile.disable()

  def print(self):
    s = io.StringIO()
    ps = pstats.Stats(self.profile, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())