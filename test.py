from nose.tools import assert_equal

from toolz.curried import map

from bookends import _


def test_creator_and_destroyer():
  assert_equal(
      _| [1, 2, 3] |_, [1, 2, 3]
  )

  assert_equal(
      (_| [1, 2, 3] |_), [1, 2, 3]
  )

  assert_equal(
      _| [1, 2, 3] | map(lambda x: x**2) | enumerate | list |_, [(0, 1), (1, 4), (2, 9)]
  )

  assert_equal(
      (_| [1, 2, 3]
        | map(lambda x: x**2)
        | enumerate
        | list
        |_),
      [(0, 1), (1, 4), (2, 9)]
  )

