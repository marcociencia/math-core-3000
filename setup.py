from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'calc_backend',
        ['calculator.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++17', '-O2'],
    ),
]

setup(
    name='calc_backend',
    version='1.0',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0'],
)
