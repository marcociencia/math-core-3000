from setuptools import setup, Extension

class get_pybind_include(object):
    """Classe auxiliar para atrasar a importação do pybind11 até que ele esteja instalado na nuvem."""
    def __str__(self):
        import pybind11
        return pybind11.get_include()

ext_modules = [
    Extension(
        'calculator_engine',
        ['calculator.cpp'],
        include_dirs=[get_pybind_include()],
        language='c++',
        extra_compile_args=['-std=c++17'],
    ),
]

setup(
    name='calculator_engine',
    version='0.1',
    ext_modules=ext_modules,
)
