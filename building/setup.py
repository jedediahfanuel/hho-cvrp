import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine-tuning.
build_options = {'packages': [], 'excludes': [
    "altgraph", "asttokens", "asyncio", "attr", "backcall", "bs4", "cairo", "certifi", "cffi",
    "colorama", "comm", "concurrent", "contourpy", "cryptography", "curses", "Cython",
    "debugpy", "defusedxml", "_distutils_hack", "docutils", "executing", "fastjsonschema",
    "gi", "ipykernel", "IPython", "jaraco", "jedi", "jinja2", "jsonschema",
    "jupyter_client", "jupyter_core", "lib2to3", "lxml", "markupsafe", "more_itertools",
    "nbformat", "ordered_set", "parso", "pexpect", "pkg_resources",
    "platformdirs", "prompt_toolkit", "psutil", "ptyprocess", "pure_eval", "pycparser",
    "pydoc_data", "pygments", "PyInstaller", "PyQt5", "pyrsistent", "pyximport",
    "setuptools", "soupsieve", "sqlite3", "stack_data", "tcl8", "tcl8.6", "tomli", "tornado", "traitlets",
    "trove_classifiers", "validate_pyproject", "wcwidth", "wheel", "xmlrpc", "zmq"
]}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, target_name='hho_cvrp', icon="./icon/hho_cvrp.ico")
]

setup(name='hho_cvrp',
      version='1.0',
      description='Penerapan Harris Hawks Optimization Pada Capacitated Vehicle Routing Problem',
      options={'build_exe': build_options},
      executables=executables)
