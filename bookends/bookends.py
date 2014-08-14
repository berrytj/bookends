from __future__ import division

import inspect
import re
from functools import wraps, partial
from collections import defaultdict
from pdb import set_trace
from copy import copy

from step import piped as step_into
from stop_as_final_func import piped as stop_as_final_func


__all__ = ('verbose', 'endverbose', 'step', 'endstep', 'stop', 'setstate', 'getstate',
           'stack', '_', 'B', 'passthrough', 'tee', 'show')


NOT_PRESENT = '__not__present__'
MAX_OPERAND_STR_LEN = 70


def identity(x):
  return x


def get_name(f):
  try:
    try:
      if isinstance(f, partial):
        return 'partial({})'.format(get_name(f.func))

      if f.__name__ == '<lambda>':
         matches = re.findall(r'\((lambda[^\|]*)\)', inspect.getsourcelines(f)[0][0])
         if len(matches) == 1:
           return matches[0]

      return f.__name__
    except AttributeError:
      return type(f).__name__
  except AttributeError:
    return '<function>'


class Options():
  def __init__(self, options, info=''):
    self.options = defaultdict(bool, options)
    self.info = info

  def __call__(self, pipe):
    pipe.options.update(self.options)
    print(self.info)

verbose = Options({'verbose': True}, 'The pipe will now print each function and its output.')
endverbose = Options({'verbose': False}, 'The pipe will no longer print each function and its output.')
step = Options({'step': True}, 'The pipe will now break before each function call.')
endstep = Options({'step': False}, 'The pipe will no longer break before each function call.')
stop = Options({'stop': True}, 'The pipe will break before the next function call.')


class setstate():
  def __init__(self, key, func=None):
    self.key = key
    if func is None:
      self.func = identity
    else:
      self.func = func

  @property
  def __name__(self):
    if self.func is identity:
      return 'setstate({})'.format(self.key)
    else:
      return 'setstate({}, {})'.format(self.key, get_name(self.func))


class getstate():
  def __init__(self, key):
    self.key = key

  def __call__(self, operand):
    return operand, self.state[self.key]

  @property
  def __name__(self):
    return 'getstate({})'.format(self.key)


class Stack():
  pass

stack = Stack()


class Bookend():
  def __init__(self, options=None):
    self.options = defaultdict(bool, options or {})

  def __or__(self, operand):
    return Pipe(operand, self.options)

_ = Bookend()
B = _
_.v = Bookend({'verbose': True})
_.s = Bookend({'step': True})
_.vs = Bookend({'verbose': True, 'step': True})
_.sv = _.vs


class Pipe():
  def __init__(self, operand, options):
    self.operand = operand
    self.options = copy(options)
    self._stack = [(None, shorten(self.operand))]
    self.state = {}

    if self.options['verbose']:
      newline()
      _print(None, self.operand)

  def __or__(self, f):
    if isinstance(f, tuple):
      f, args = f[0], f[1:]
      return self.__or__(partial(f, *args))
    
    if isinstance(f, Bookend):
      if self.options['stop']:
        self.operand = stop_as_final_func(self.operand, self)
      if self.options['verbose']:
        newline()
      return self.operand

    if isinstance(f, Options):
      self.options.update(f.options)
      if 'verbose' in f.options:
        newline()
      return self

    if isinstance(f, Stack):
      print('Stack:')
      self.stack()
      return self

    if isinstance(f, setstate):
      self.state[f.key] = f.func(self.operand)
      self._stack.append((get_name(f), NOT_PRESENT))
      return self

    if isinstance(f, getstate):
      f.state = self.state

    try:
      if self.options['step'] or self.options['stop']:
        self.options['stop'] = False
        self.operand = step_into(f, self.operand, self)
      else:
        self.operand = f(self.operand)
    except Exception as e:
      self._stack.append((get_name(f), '** {}: {} **'.format(type(e).__name__, e.message)))
      print('Pipe traceback:')
      self.stack()
      raise

    if not getattr(f, 'is_passthrough', False):
      name = get_name(f)
      self._stack.append((name, shorten(self.operand)))
      if self.options['verbose']:
        _print(name, self.operand)

    return self

  def stack(self):
    [_print(func, output) for func, output in self._stack]
    newline()

  def verbose(self): verbose(self)
  def endverbose(self): endverbose(self)
  def step(self): step(self)
  def endstep(self): endstep(self)
  def stop(self): stop(self)


def passthrough(f):
  """E.g. for log or inc."""
  @wraps(f)
  def wrapped(operand):
    f(operand)
    return operand
  wrapped.is_passthrough = True
  return wrapped

tee = passthrough


@passthrough
def show(operand):
  print('Operand:')
  _print(None, shorten(operand))
  newline()


def _print(function_name, operand):
  bar = '|'
  arrow = '=>'
  if function_name is None:
    print('{} {}'.format(bar, operand))
  elif operand == NOT_PRESENT:
    print('{} {}'.format(bar, function_name))
  else:
    max_line_length = 70
    line_length = sum(map(len, map(str, [bar, function_name, arrow, operand])))
    if line_length > max_line_length:
      delimeter = '\n' + (' ' * 6)
    else:
      delimeter = ' '
    print('{} {} {}{}{}'.format(bar, function_name, arrow, delimeter, operand))


def newline():
  print('')


def shorten(operand):
  operand = str(operand)
  if len(operand) > MAX_OPERAND_STR_LEN:
    segment_len = int(MAX_OPERAND_STR_LEN / 2) - 2
    operand = '{}...{}'.format(operand[:segment_len], operand[-segment_len:])
  return operand

