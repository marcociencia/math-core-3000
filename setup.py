from setuptools import setup, Extension
import pybind11
import sys
import os

# Força recompilação no Streamlit Cloud
if 'STREAMLIT_SHARING' in os.environ or 'STREAMLIT_CLOUD' in os.environ:
    # Streamlit Cloud precisa de flags específicas
    extra_compile_args = ['-std=c++11', '-O2', '-fPIC']
else:
    extra_compile_args = ['-std=c++11']

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
    install_requires=['pybind11>=2.10.0'],
)
