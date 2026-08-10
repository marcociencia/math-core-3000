#include <pybind11/pybind11.h>
#include <stdexcept>
#include <cmath>
#include <string>

namespace py = pybind11;

class AdvancedCalculator {
public:
    double add(double a, double b) { return a + b; }
    double subtract(double a, double b) { return a - b; }
    double multiply(double a, double b) { return a * b; }
    double divide(double a, double b) { 
        if (b == 0.0) throw std::invalid_argument("Division by zero error!");
        return a / b; 
    }
    double power(double base, double exp) { return std::pow(base, exp); }
    double sqrt_num(double a) { 
        if (a < 0) throw std::invalid_argument("Cannot calculate square root of negative number!");
        return std::sqrt(a); 
    }
    double percentage(double a, double b) { return (a * b) / 100.0; }
    long long factorial(int n) {
        if (n < 0) throw std::invalid_argument("Factorial of negative number!");
        if (n > 20) throw std::invalid_argument("Number too large!");
        long long result = 1;
        for(int i = 2; i <= n; i++) result *= i;
        return result;
    }
};

PYBIND11_MODULE(calc_backend, m) {
    py::class_<AdvancedCalculator>(m, "AdvancedCalculator")
        .def(py::init<>())
        .def("add", &AdvancedCalculator::add)
        .def("subtract", &AdvancedCalculator::subtract)
        .def("multiply", &AdvancedCalculator::multiply)
        .def("divide", &AdvancedCalculator::divide)
        .def("power", &AdvancedCalculator::power)
        .def("sqrt", &AdvancedCalculator::sqrt_num)
        .def("percentage", &AdvancedCalculator::percentage)
        .def("factorial", &AdvancedCalculator::factorial);
}
