from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': ["Cython", "PyQt5"]}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'hho_cvrp')
]

setup(name='hho_cvrp',
      version = '1.0',
      description = 'Penerapan Harris Hawks Optimization Pada Capacitated Vehicle Routing Problem',
      options = {'build_exe': build_options},
      executables = executables)
