import stop

def piped(f, operand, pipe):
  """
  Try pipe.stack(), pipe.verbose(), pipe.endstep().
  """
  stop()
  result = f(operand)
  return result
