#!/usr/bin/python3

import argparse
import os.path
import sys
import threading
import warnings
import webbrowser

try:
    from notebook import notebookapp
    from notebook.utils import url_path_join, url_escape
except ImportError:
    from IPython.html import notebookapp
    from IPython.html.utils import url_path_join, url_escape

__version__ = '0.3'

def find_best_server(filename, profile='default'):
    kwargs = {}
    if profile != 'default':
        warnings.warn("Jupyter doesn't have profiles")
        kwargs['profile'] = profile
    servers = [si for si in notebookapp.list_running_servers(**kwargs) \
               if filename.startswith(si['notebook_dir'])]
    try:
        return max(servers, key=lambda si: len(si['notebook_dir']))
    except ValueError:
        return None


def nbopen(filename, profile='default', query=''):

    def open_notebook(filename, profile):
        filename = os.path.abspath(filename)
        home_dir = os.path.expanduser('~')
        server_inf = find_best_server(filename, profile)
        if server_inf is not None:
            print("Using existing server at", server_inf['notebook_dir'])
            path = os.path.relpath(filename, start=server_inf['notebook_dir'])
            url = url_path_join(server_inf['url'], 'notebooks', url_escape(path))
            if query:
                url = '{}?{}'.format(url, query)
            na = notebookapp.NotebookApp.instance()
            na.load_config_file()
            browser = webbrowser.get(na.browser or None)
            browser.open(url, new=2)
        else:
            raise ValueError('no server available')

    filename = os.path.abspath(filename)
    home_dir = os.path.expanduser('~')
    server_inf = find_best_server(filename, profile)

    if server_inf is None:
        # We could introduce a check, rather than a wait; though this adds
        # code complication.
        twait = 4
        # Open the  requested notebook in the server, once it has opened.
        t = threading.Timer(twait, open_notebook, args=[filename, profile])
        t.start()
        print('z' * twait)

        if filename.startswith(home_dir):
            nbdir = home_dir
        else:
            nbdir = os.path.dirname(filename)

        print("Starting new server")
        notebookapp.launch_new_instance(notebook_dir=nbdir,
                                        open_browser=False,
                                        argv=[],  # Avoid it seeing our own argv
            )
    else:
        open_notebook(filename, profile)
        

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--profile', default='default',
                    help=argparse.SUPPRESS)
    ap.add_argument('filename', help='The notebook file to open')
    ap.add_argument('-q', '--query', default='',
                    help='query string for the notebook url')
    args = ap.parse_args(argv)

    nbopen(args.filename, args.profile, args.query)

if __name__ == '__main__':
    main()
