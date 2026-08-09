from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'calculator_engine',
        ['calculator.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name='calculator_engine',
    version='0.1',
    ext_modules=ext_modules,
)