#!/usr/bin/python3

import argparse
import os.path
import sys
import warnings
import webbrowser

try:
    from jupyter_notebook import notebookapp
    from jupyter_notebook.utils import url_path_join
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

class OutsideHomeDir(ValueError): pass

def nbopen(filename, profile='default'):
    filename = os.path.abspath(filename)
    home_dir = os.path.expanduser('~')
    server_inf = find_best_server(filename, profile)
    if server_inf is not None:
        print("Using existing server at", server_inf['notebook_dir'])
        path = os.path.relpath(filename, start=server_inf['notebook_dir'])
        url = url_path_join(server_inf['url'], 'notebooks', path)
        webbrowser.open(url, new=2)
    elif filename.startswith(home_dir):
        print("Starting new server")
        filename = os.path.abspath(filename)
        if os.path.isdir(filename):
            kw = {'notebook_dir': filename}
        else:
            kw = {'file_to_run': filename}
        notebookapp.launch_new_instance(open_browser=True,
                                        argv=[],  # Avoid it seeing our own argv
                                        **kw
                                       )
    else:
        raise OutsideHomeDir

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--profile', default='default',
                    help=argparse.SUPPRESS)
    ap.add_argument('filename', help='The notebook file to open')
    
    args = ap.parse_args(argv)
    try:
        nbopen(args.filename, args.profile)
    except OutsideHomeDir:
        sys.exit("I don't currently open notebooks outside your home directory, "
                 "for security reasons.")

if __name__ == '__main__':
    main()
