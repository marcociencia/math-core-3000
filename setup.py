from setuptools import setup, Extension
import pybind11
import sys

# Compiler flags for better compatibility
extra_compile_args = ['-std=c++17']
if sys.platform == 'linux':
    extra_compile_args.extend(['-O2', '-fPIC'])

ext_modules = [
    Extension(
        'calc_backend',
        ['calculator.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=extra_compile_args,
    ),
]

setup(
    name='calc_backend',
    version='1.0.0',
    description='Advanced Calculator with C++ Backend',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0'],
    python_requires='>=3.7',
)
