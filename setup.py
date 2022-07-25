import os
import sys
from cx_Freeze import setup, Executable



import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], "include_files" : ["DSTASPXN.csv", "minus.png", "plus.png"]}
# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['DSTASPXN.csv', 'minus.png', 'plus.png']

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="CSV Editor",
    version="0.1",
    description="CSV Editor application",
    options={"build_exe": build_exe_options},
    executables=[Executable("csv_editor.py", base=base, icon='icon.ico')],
)
