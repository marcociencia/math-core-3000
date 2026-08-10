from setuptools import setup, Extension

class get_pybind_include(object):
    def __str__(self):
        import pybind11
        return pybind11.get_include()

ext_modules = [
    Extension(
        'calc_backend',
        ['calculator.cpp'],
        include_dirs=[get_pybind_include()],
        language='c++',
        extra_compile_args=['-std=c++17'],
    ),
]

setup(
    name='calc_backend',
    version='1.0',
    ext_modules=ext_modules,
)
