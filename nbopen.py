#!/usr/bin/python3

import argparse
import os.path
import sys
import warnings
import webbrowser

try:
    from notebook import notebookapp
    from notebook.utils import url_path_join
except ImportError:
    from IPython.html import notebookapp
    from IPython.html.utils import url_path_join

__version__ = '0.2'

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


def nbopen(filename, profile='default'):
    filename = os.path.abspath(filename)
    home_dir = os.path.expanduser('~')
    server_inf = find_best_server(filename, profile)
    if server_inf is not None:
        print("Using existing server at", server_inf['notebook_dir'])
        path = os.path.relpath(filename, start=server_inf['notebook_dir'])
        url = url_path_join(server_inf['url'], 'notebooks', path)
        webbrowser.open(url, new=2)
    else:
        if filename.startswith(home_dir):
            nbdir = home_dir
        else:
            nbdir = os.path.dirname(filename)

        print("Starting new server")
        notebookapp.launch_new_instance(file_to_run=os.path.abspath(filename),
                                        notebook_dir=nbdir,
                                        open_browser=True,
                                        argv=[],  # Avoid it seeing our own argv
                                       )

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--profile', default='default',
                    help=argparse.SUPPRESS)
    ap.add_argument('filename', help='The notebook file to open')
    
    args = ap.parse_args(argv)

    nbopen(args.filename, args.profile)

if __name__ == '__main__':
    main()
