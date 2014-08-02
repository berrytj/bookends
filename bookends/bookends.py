class Bookend():
  def __or__(self, operand):
    return Piped(operand)


class Piped():
  def __init__(self, operand):
    self.operand = operand

  def __or__(self, f):
    if isinstance(f, Bookend):
      return self.operand
    else:
      return Piped(f(self.operand))


_ = Bookend()

