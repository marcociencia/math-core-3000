class AdvancedCalculator:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0: raise ZeroDivisionError("Division by zero!")
        return a / b
    def power(self, a, b): return a ** b
