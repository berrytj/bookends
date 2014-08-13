A simple syntax for piping in Python.

Compare:

.. code-block:: python

  from bookends import _
  from toolz.curried import map

  l = _| [3, 2, 1] | map(lambda n: n*2) | sorted |_   # [2, 4, 6]

with:

.. code-block:: python

  l = sorted(map(lambda n: n*2, [3, 2, 1]))

  l = sorted([n*2 for n in [3, 2, 1]])

  l = []
  for n in [3, 2, 1]:
      l.append(n*2)
  l.sort()
  
For an extended comparison, see `example.py <https://github.com/berrytj/bookends/blob/master/example.py>`_.


To install:

.. code-block:: python

  pip install bookends


To use:

.. code-block:: python

  from bookends import _


For similar tools, see:

- `from fn import F <https://github.com/kachayev/fn.py>`_
- `from toolz import thread_first, thread_last <http://toolz.readthedocs.org/en/latest/api.html?highlight=thread_first#toolz.functoolz.thread_first>`_, `pipe <http://toolz.readthedocs.org/en/latest/api.html#toolz.functoolz.pipe>`_
- `Clojure's -> and ->> <http://clojure.github.io/clojure/clojure.core-api.html#clojure.core/-%3e>`_
- `Underscore's chain <http://underscorejs.org/#chain>`_
- Unix |


Note: for multiline usage, wrap the expression in parens.

.. code-block:: python

  import csv
  from StringIO import StringIO

  (_| '40,5,10\n20,6,9\n41,10,10\n'
    | StringIO
    | csv.reader
    | sorted
    |_)

  # [['20', '6', '9'], ['40', '5', '10'], ['41', '10', '10']]
            

Wrap lone lambdas in parens as well.

.. code-block:: python
  
  (_| ['addition', 'multiplication']
    | (lambda l: l + ['exponentiation', 'tetration'])
    | ', '.join
    |_)

  # 'addition, multiplication, exponentiation, tetration'


You can use partial or `curried <http://toolz.readthedocs.org/en/latest/curry.html>`_ functions.

.. code-block:: python
  
  from functools import partial
  from toolz.curried import drop

  (_| ['ca', 'tx', 'ny']
    | partial(map, lambda state: state.upper())
    | drop(1)
    | list
    |_)

  # ['TX', 'NY']


And/or use `threading <http://toolz.readthedocs.org/en/latest/api.html#toolz.functoolz.thread_last>`_ syntax, by putting each function and its arguments into a tuple.

.. code-block:: python
  
  from toolz import drop

  (_| ['ca', 'tx', 'ny']
    | (map, lambda state: state.upper())
    | (drop, 1)
    | list
    |_)

  # ['TX', 'NY']


If you don't like the underscore, import the bookend as B.

.. code-block:: python
  
  from bookends import B

  (B| ['ca', 'tx', 'ny']
    | (map, lambda state: state.upper())
    | (drop, 1)
    | list
    |B)


Plays nice with `Kachayev's _ <https://github.com/kachayev/fn.py>`_.

.. code-block:: python
  
  from fn import _ as __

  _| [1, 2, 3] | __ + [4, 5] |_

  # [1, 2, 3, 4, 5]


Here's a simplified version of the source:

.. code-block:: python

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
        self.operand = f(self.operand)
        return self


  _ = Bookend()


Contact: `@bzrry <https://twitter.com/bzrry>`_.

