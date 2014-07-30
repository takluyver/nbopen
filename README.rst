Open notebooks from the command line

nbopen looks for the nearest running notebook server - if it finds one, it
opens a web browser to that notebook. If not, it starts a new notebook server
in that directory.

Installation::

    pip install nbopen

Usage::

    nbopen AwesomeNotebook.ipynb

To integrate with Linux/BSD file managers, so you can double click on notebooks
to open them, clone the repository and run ``./xdg-install.sh``.
