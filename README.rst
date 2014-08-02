A simple syntax for piping in Python.

Compare:

.. code-block:: python

  from bookends import _
  from toolz.curried import map

  l = _| [1, 2, 3] | map(lambda n: n*2) |_

.. code-block:: python

  l = map(lambda n: n*2, [1, 2, 3])

  l = [n*2 for n in [1, 2, 3]]

  l = []
  for n in [1, 2, 3]:
    l.append(n*2)
  
For an extended example, see `example.py <https://github.com/berrytj/bookends/blob/master/example.py>`_.


For similar tools, see:

- from fn import F
- from toolz import thread_first, thread_last
- Clojure's -> and ->>
- Unix |


Note: for multiline usage, wrap the expression in parens.

.. code-block:: python

  from bookends import _
  from toolz.curried import map

  l = (_| [1, 2, 3]
        | map(lambda n: n*2)
        | map(lambda n: n**3)
        |_)


Here's the entire source:

.. code-block:: python

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


Contact: `@bzrry <https://twitter.com/bzrry>`_.

