import streamlit as st
import calculator_engine

st.set_page_config(page_title="Math Core 3000", page_icon="🧮")
st.title("🧮 Math Core 3000")
st.subheader("High-Performance Backend by C++")

calc = calculator_engine.Calculator()

col1, col2 = st.columns(2)
a = col1.number_input("Number 1", value=0.0)
b = col2.number_input("Number 2", value=0.0)

op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])

if st.button("Calculate"):
    try:
        if op == "Add": res = calc.add(a, b)
        elif op == "Subtract": res = calc.subtract(a, b)
        elif op == "Multiply": res = calc.multiply(a, b)
        elif op == "Divide": res = calc.divide(a, b)
        st.success(f"Result: {res}")
    except Exception as e:
        st.error(f"Error: {e}")