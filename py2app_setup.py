#!/usr/bin/python3
import sys
from setuptools import setup  # Noooooo

import nbopen


if sys.platform != 'darwin':
    sys.exit('This script runs on OS X only.')

Plist = dict(CFBundleName='nbopen',
        CFBundleShortVersionString='0.2',
        CFBundleVersion='0.2',
        CFBundleIdentifier='org.jupyter.nbopen',
        CFBundleDevelopmentRegion='English',
        CFBundleDocumentTypes=[dict(CFBundleTypeExtensions=["ipynb"],
                                 CFBundleTypeName="IPython Notebook",
                                 CFBundleTypeIconFile="nbopen",
                                 CFBundleTypeRole="Editor"),
                            ]
     )

setup(name='nbopen',
      version=nbopen.__version__,
      description="Open a notebook from the command line in the best available server",
      author='Thomas Kluyver',
      author_email="thomas@kluyver.me.uk",
      url="https://github.com/takluyver/nbopen",
      app=['nbopen.py'],  # FIXME: What should this be, py2app users?
      options={'py2app': {
          'argv_emulation': True,
          'packages': ['nbopen'],
          'alias': True,
          'plist': Plist,
          'iconfile': 'nbopen.icns'
      }},
      setup_requires=['py2app']
)

