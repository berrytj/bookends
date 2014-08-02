#!/usr/bin/env python

from os.path import exists
from setuptools import setup

import bookends


setup(name='bookends',
      version=bookends.__version__,
      description='A simple piping syntax',
      url='http://github.com/berrytj/bookends',
      author='Tom Berry',
      maintainer='Tom Berry',
      maintainer_email='tberry860@gmail.com',
      license='MIT',
      keywords='functional pipe',
      packages=['bookends'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)

