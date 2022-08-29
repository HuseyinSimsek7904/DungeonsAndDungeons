import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["libs"], "excludes": []}
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="DungeonsAndDungeons.exe",
    version="0.1",
    description="",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)
