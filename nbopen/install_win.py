"""Install GUI integration on Windows"""

import sys

try:
  import winreg
except ImportError:  
  import _winreg as winreg

SZ = winreg.REG_SZ
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\Classes\.ipynb") as k:
    winreg.SetValue(k, "", SZ, "Jupyter.nbopen")
    winreg.SetValueEx(k, "Content Type", 0, SZ, "application/x-ipynb+json")
    winreg.SetValueEx(k, "PerceivedType", 0, SZ, "document")
    with winreg.CreateKey(k, "OpenWithProgIds") as openwith:
        winreg.SetValueEx(openwith, "Jupyter.nbopen", 0, winreg.REG_NONE, b'')

executable = sys.executable
if executable.endswith("python.exe"):
    executable = executable[:-10] + 'pythonw.exe'
launch_cmd = '"{}" -m nbopen "%1"'.format(executable)

with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\Classes\Jupyter.nbopen") as k:
    winreg.SetValue(k, "", SZ, "IPython notebook")
    with winreg.CreateKey(k, "shell\open\command") as launchk:
        winreg.SetValue(launchk, "", SZ, launch_cmd)

try:
    from win32com.shell import shell, shellcon
    shell.SHChangeNotify(shellcon.SHCNE_ASSOCCHANGED, shellcon.SHCNF_IDLIST, None, None)
except ImportError:
    print("You may need to restart for association with .ipynb files to work")
    print("  (pywin32 is needed to notify Windows of the change)")
