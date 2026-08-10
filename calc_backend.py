class AdvancedCalculator:
    """Advanced Calculator with high precision operations"""
    
    def add(self, a: float, b: float) -> float:
        """Addition operation"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtraction operation"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication operation"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Division with zero check"""
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed!")
        return a / b
    
    def power(self, base: float, exp: float) -> float:
        """Power operation"""
        return base ** exp
    
    def sqrt(self, a: float) -> float:
        """Square root with negative check"""
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number!")
        return a ** 0.5
    
    def percentage(self, a: float, b: float) -> float:
        """Calculate percentage: a% of b"""
        return (a * b) / 100.0
    
    def factorial(self, n: int) -> int:
        """Factorial with validation"""
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers!")
        if n > 1000:
            raise ValueError("Number too large! Maximum is 1000")
        result = 1
        for i in range(2, int(n) + 1):
            result *= i
        return result
    
    def sin(self, angle: float) -> float:
        """Sine of angle in degrees"""
        import math
        return math.sin(math.radians(angle))
    
    def cos(self, angle: float) -> float:
        """Cosine of angle in degrees"""
        import math
        return math.cos(math.radians(angle))
    
    def log(self, a: float, base: float = 10) -> float:
        """Logarithm with custom base"""
        import math
        if a <= 0:
            raise ValueError("Logarithm only defined for positive numbers!")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base!")
        return math.log(a, base)
