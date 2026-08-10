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
        if (b == 0.0) throw std::invalid_argument("Division by zero error!");
        return a / b; 
    }
    double power(double base, double exp) { return std::pow(base, exp); }
};

PYBIND11_MODULE(calc_backend, m) {
    py::class_<AdvancedCalculator>(m, "AdvancedCalculator")
        .def(py::init<>())
        .def("add", &AdvancedCalculator::add)
        .def("subtract", &AdvancedCalculator::subtract)
        .def("multiply", &AdvancedCalculator::multiply)
        .def("divide", &AdvancedCalculator::divide)
        .def("power", &AdvancedCalculator::power);
}
