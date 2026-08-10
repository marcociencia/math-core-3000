import os
import sys
import ctypes
import platform

class AdvancedCalculator:
    """Wrapper que tenta usar C++ compilado, com fallback Python"""
    
    def __init__(self):
        self.use_cpp = False
        self._try_load_cpp()
    
    def _try_load_cpp(self):
        """Tenta carregar biblioteca C++ pré-compilada"""
        try:
            # Tenta importar pybind11
            import calc_backend as cpp_module
            self.cpp_calc = cpp_module.AdvancedCalculator()
            self.use_cpp = True
        except:
            # Tenta carregar .so/.dll diretamente
            try:
                lib_name = self._get_lib_name()
                if os.path.exists(lib_name):
                    # Carrega biblioteca compartilhada
                    self.cpp_lib = ctypes.CDLL(f"./{lib_name}")
                    self.use_cpp = True
            except:
                pass
    
    def _get_lib_name(self):
        """Retorna nome da biblioteca conforme SO"""
        system = platform.system()
        if system == "Linux":
            return "calc_backend.cpython-*-linux-gnu.so"
        elif system == "Windows":
            return "calc_backend.pyd"
        elif system == "Darwin":
            return "calc_backend.cpython-*-darwin.so"
        return None
    
    def add(self, a, b):
        if self.use_cpp:
            return self.cpp_calc.add(a, b)
        return a + b
    
    def subtract(self, a, b):
        if self.use_cpp:
            return self.cpp_calc.subtract(a, b)
        return a - b
    
    def multiply(self, a, b):
        if self.use_cpp:
            return self.cpp_calc.multiply(a, b)
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero!")
        if self.use_cpp:
            return self.cpp_calc.divide(a, b)
        return a / b
    
    def power(self, a, b):
        if self.use_cpp:
            return self.cpp_calc.power(a, b)
        return a ** b
    
    def sqrt(self, a):
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number!")
        if self.use_cpp:
            return self.cpp_calc.sqrt(a)
        return a ** 0.5
    
    def percentage(self, a, b):
        if self.use_cpp:
            return self.cpp_calc.percentage(a, b)
        return (a * b) / 100.0
