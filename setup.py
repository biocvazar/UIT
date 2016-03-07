# chardet's setup.py
# from distutils.core import setup
import sys
from cx_Freeze import setup, Executable

setup(
    name="BDLab",
    version="0.1",
    description="Communication",
    executables=[Executable("I:\\Project\\UIT\\UIT\\task.py", base="Win32GUI")]
)

