A simple syntax for piping in Python.


For similar tools, see:

Unix's |

from fn import F

from toolz import thread_first, thread_last

Clojure's -> and ->>

etc.


Compare:

l = []
for n in [1, 2, 3]:
  l.append(n*2)

l = [n*2 for n in [1, 2, 3]]

l = map(lambda n: n*2, [1, 2, 3])
  
from bookends import _
from toolz.curried import map

l = _| [1, 2, 3] | map(lambda n: n*2) |_
  
See example.py for an extended example.


Here's the entire source:

class CreatorAndDestroyer():
  def __or__(self, operand):
    return Piped(operand)


class Piped():
  def __init__(self, operand):
    self.operand = operand

  def __or__(self, f):
    if isinstance(f, CreatorAndDestroyer):
      return self.operand
    else:
      return Piped(f(self.operand))


_ = CreatorAndDestroyer()


Contact: @bzrry

