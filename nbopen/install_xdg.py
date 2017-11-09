"""Install GUI integration on XDG platforms (primarily Linux)"""
import os
from pathlib import Path
import shutil
from subprocess import call, CalledProcessError

_PKGDIR = Path(__file__).resolve().parent

if not os.environ.get('XDG_DATA_HOME'):
    os.environ['XDG_DATA_HOME'] = os.path.expanduser('~/.local/share')
print("Installing data files to:", os.environ['XDG_DATA_HOME'])

#export XDG_UTILS_DEBUG_LEVEL=1  #DEBUG

print('Installing mimetype data...')
if call(['xdg-mime', 'install', str(_PKGDIR / 'application-x-ipynb+json.xml')]) != 0:
    raise CalledProcessError

print('Installing icons...')
for s in [16, 24, 32, 48, 64, 128, 256, 512]:
    src = _PKGDIR / "icons/ipynb_icon_{s}x{s}.png".format(s=s)
    if call(['xdg-icon-resource', 'install', '--noupdate', '--size', str(s),
         '--context', 'mimetypes', str(src), 'application-x-ipynb+json']) != 0:
         raise CalledProcessError

if call(['xdg-icon-resource', 'forceupdate']) != 0:
    raise CalledProcessError

print('Installing desktop file...')
apps_dir = os.path.join(os.environ['XDG_DATA_HOME'], "applications/")
shutil.copy2(str(_PKGDIR / 'nbopen.desktop'), apps_dir)
if call(['update-desktop-database', apps_dir]) != 0:
    raise CalledProcessError
