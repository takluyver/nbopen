#!/usr/bin/python3
import sys
from distutils.core import setup


def main(argv=None):
    if argv is not None:
        # sarcastic message about distutils here
        saved_argv = sys.argv[:]
        sys.argv[1:] = argv

    if sys.platform == 'darwin':
        import setuptools
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
        extra_options = dict(
            app=['nbopen.py'],
            options={'py2app': {
                'argv_emulation': True,
                'packages': ['nbopen'],
                'alias': True,
                'plist': Plist,
                'iconfile': 'nbopen.icns'
            }},
            setup_requires=['py2app']
        )

    else:
        extra_options = {}

    try:
        with open('README.rst') as f:
            readme = f.read()

        setup(name='nbopen',
              version='0.3',
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
             **extra_options)

    finally:
        if argv is not None:
            sys.argv = saved_argv

if __name__ == '__main__':
    main()
