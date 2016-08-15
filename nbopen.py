#!/usr/bin/python3

import argparse
import os.path
import warnings
import webbrowser

try:
    from notebook import notebookapp
    from notebook.utils import url_path_join, url_escape
    import nbformat
except ImportError:
    from IPython import nbformat
    from IPython.html import notebookapp
    from IPython.html.utils import url_path_join, url_escape

__version__ = '0.3'

def find_best_server(filename, profile='default'):
    kwargs = {}
    if profile != 'default':
        warnings.warn("Jupyter doesn't have profiles")
        kwargs['profile'] = profile
    servers = [si for si in notebookapp.list_running_servers(**kwargs)
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
    if os.path.exists(filename):
        msg = "Notebook {} already exists"
        print(msg.format(filename))
        print("Opening existing notebook")
    elif os.path.exists(filename + '.ipynb'):
        msg = "A Notebook {} with extension .ipynb already exists"
        print(msg.format(filename))
        print("Opening existing notebook")
        filename += '.ipynb'
    else:
        if not filename.endswith('.ipynb'):
            filename += '.ipynb'
        nb_version = nbformat.versions[nbformat.current_nbformat]
        nbformat.write(nb_version.new_notebook(),
                       filename)
    return filename

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--profile', default='default',
                    help=argparse.SUPPRESS)
    ap.add_argument('-n', '--new', action='store_true', default=False)
    ap.add_argument('filename', help='The notebook file to open')

    args = ap.parse_args(argv)

    if args.new:
        filename = nbnew(args.filename)
    else:
        filename = args.filename

    nbopen(filename, args.profile)

if __name__ == '__main__':
    main()
