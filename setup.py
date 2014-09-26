#!/usr/bin/python3
import sys
from distutils.core import setup

def main(argv=None):
    if argv is not None:
        # sarcastic message about distutils here
        saved_argv = sys.argv[:]
        sys.argv[1:] = argv

    try:
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
              scripts=['nbopen'],
              classifiers=[
                  "Framework :: IPython",
                  "License :: OSI Approved :: BSD License",
                  "Programming Language :: Python :: 2",
                  "Programming Language :: Python :: 3",
                 ],
             )

    finally:
        if argv is not None:
            sys.argv = saved_argv

if __name__ == '__main__':
    main()
