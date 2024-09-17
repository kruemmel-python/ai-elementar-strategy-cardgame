# Datei: setup.py

from setuptools import setup
from Cython.Build import cythonize
import numpy

# Kompiliere die Cython-Datei
setup(
    ext_modules=cythonize("dataprocessing.pyx"),
    include_dirs=[numpy.get_include()]
)
