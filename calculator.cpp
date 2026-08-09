#include <pybind11/pybind11.h>

namespace py = pybind11;

class Calculator {
public:
    double add(double a, double b) { return a + b; }
    double subtract(double a, double b) { return a - b; }
    double multiply(double a, double b) { return a * b; }
    double divide(double a, double b) { 
        if (b == 0) throw std::invalid_argument("Division by zero!");
        return a / b; 
    }
};

PYBIND11_MODULE(calculator_engine, m) {
    py::class_<Calculator>(m, "Calculator")
        .def(py::init<>())
        .def("add", &Calculator::add)
        .def("subtract", &Calculator::subtract)
        .def("multiply", &Calculator::multiply)
        .def("divide", &Calculator::divide);
}