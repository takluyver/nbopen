#!/usr/bin/python3

import argparse
import os.path
import webbrowser

from notebook import notebookapp
from notebook.utils import url_path_join, url_escape
import nbformat

def find_best_server(filename):
    servers = [si for si in notebookapp.list_running_servers()
               if filename.startswith(si['notebook_dir'])]
    try:
        return max(servers, key=lambda si: len(si['notebook_dir']))
    except ValueError:
        return None


def nbopen(filename):
    filename = os.path.abspath(filename)
    home_dir = os.path.expanduser('~')
    server_inf = find_best_server(filename)
    if server_inf is not None:
        print("Using existing server at", server_inf['notebook_dir'])
        path = os.path.relpath(filename, start=server_inf['notebook_dir'])
        if os.sep != '/':
            path = path.replace(os.sep, '/')
        url = url_path_join(server_inf['url'], 'notebooks', url_escape(path))
        na = notebookapp.NotebookApp.instance()
        na.load_config_file()
        browser = webbrowser.get(na.browser or None)
        browser.open(url, new=2)
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
