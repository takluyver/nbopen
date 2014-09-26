#!/usr/bin/python3

from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(name='nbopen',
      version='0.2',
      description="Open a notebook from the command line in the best available server",
      long_description=readme,
      author='Thomas Kluyver',
      author_email="thomas@kluyver.me.uk",
      url="https://github.com/takluyver/nbopen",
      py_modules=['nbopen'],
      scripts=['nbopen.py'],
      classifiers=[
          "Framework :: IPython",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
         ],
     )