#include <pybind11/pybind11.h>
#include <stdexcept>
#include <cmath>

namespace py = pybind11;

class AdvancedCalculator {
public:
    double add(double a, double b) { return a + b; }
    double subtract(double a, double b) { return a - b; }
    double multiply(double a, double b) { return a * b; }
    double divide(double a, double b) { 
        if (b == 0.0) throw std::invalid_argument("Division by zero!");
        return a / b; 
    }
    double power(double base, double exp) { return std::pow(base, exp); }
    double sqrt_num(double a) { 
        if (a < 0) throw std::invalid_argument("Negative square root!");
        return std::sqrt(a); 
    }
    double cbrt(double a) { 
        return std::cbrt(a);  // C++17 já tem cbrt!
    }
    double percentage(double a, double b) { return (a * b) / 100.0; }
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
        .def("cbrt", &AdvancedCalculator::cbrt)
        .def("percentage", &AdvancedCalculator::percentage);
}
