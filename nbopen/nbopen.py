#!/usr/bin/python3

import argparse
import os.path
import webbrowser

from jupyter_server import serverapp
from jupyter_server.utils import url_path_join, url_escape
from notebook import app as notebookapp
import nbformat
from traitlets.config import Config

def find_best_server(filename):
    servers = [si for si in serverapp.list_running_servers()
               if filename.startswith(si['root_dir'])]
    try:
        return max(servers, key=lambda si: len(si['root_dir']))
    except ValueError:
        return None


def nbopen(filename):
    filename = os.path.abspath(filename)
    home_dir = os.path.expanduser('~')
    server_inf = find_best_server(filename)
    if server_inf is not None:
        print("Using existing server at", server_inf['root_dir'])
        path = os.path.relpath(filename, start=server_inf['root_dir'])
        if os.sep != '/':
            path = path.replace(os.sep, '/')
        urlseg = 'tree' if os.path.isdir(filename) else 'notebooks'
        url = url_path_join(server_inf['url'], urlseg, url_escape(path))
        sa = serverapp.ServerApp.instance()
        sa.load_config_file()
        browser = webbrowser.get(sa.browser or None)
        browser.open(url, new=2)
    else:
        if filename.startswith(home_dir):
            nbdir = home_dir
        else:
            nbdir = os.path.dirname(filename)

        print("Starting new server")
        # Hack: we want to override these settings if they're in the config file.
        # The application class allows 'command line' config to override config
        # loaded afterwards from the config file. So by specifying argv, we
        # can use this mechanism.
        argv = ["--ServerApp.file_to_run", os.path.abspath(filename),
                "--ServerApp.root_dir", nbdir,
                "--ServerApp.open_browser", "True"]
        notebookapp.launch_new_instance(argv=argv)

def nbnew(filename):
    if not filename.endswith('.ipynb'):
        filename += '.ipynb'
    if os.path.exists(filename):
        msg = "Notebook {} already exists"
        print(msg.format(filename))
        print("Opening existing notebook")
    else:
        nb_version = nbformat.versions[nbformat.current_nbformat]
        nbformat.write(nb_version.new_notebook(),
                       filename)
    return filename

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--new', action='store_true', default=False,
                    help='Create a new notebook file with the given name.')
    ap.add_argument('filename', help='The notebook file to open')

    args = ap.parse_args(argv)
    if args.new:
        filename = nbnew(args.filename)
    else:
        filename = args.filename

    nbopen(filename)

if __name__ == '__main__':
    main()
