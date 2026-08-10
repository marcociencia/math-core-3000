import streamlit as st
import time

# Tenta importar C++, senão usa Python
try:
    import calc_backend
    calc = calc_backend.AdvancedCalculator()
    backend_type = "C++"
except:
    # Fallback Python
    class PythonCalc:
        def add(self, a, b): return a + b
        def subtract(self, a, b): return a - b
        def multiply(self, a, b): return a * b
        def divide(self, a, b):
            if b == 0: raise ZeroDivisionError("Division by zero!")
            return a / b
        def power(self, a, b): return a ** b
        def sqrt(self, a):
            if a < 0: raise ValueError("Negative square root!")
            return a ** 0.5
        def percentage(self, a, b): return (a * b) / 100.0
    
    calc = PythonCalc()
    backend_type = "Python"

# Configuração da página
st.set_page_config(page_title="Math Core 3000", page_icon="🧮", layout="centered")

# CSS Elegante
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0E1117 0%, #1A1B23 100%); }
    .main-title { color: #6C63FF; text-align: center; font-size: 3rem; font-weight: 700; }
    .result-box { background: rgba(108, 99, 255, 0.1); border: 2px solid #6C63FF; 
                  border-radius: 15px; padding: 1.5rem; text-align: center; margin: 1.5rem 0; }
    .result-number { color: #6C63FF; font-size: 2.5rem; font-weight: 700; }
    .stButton>button { background: linear-gradient(135deg, #6C63FF, #4834D4); color: white; 
                       border: none; border-radius: 10px; padding: 0.8rem; width: 100%; 
                       font-size: 1.1rem; font-weight: 600; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(108, 99, 255, 0.4); }
    .badge { padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
    .badge-cpp { background: #6C63FF; color: white; }
    .badge-python { background: #FFC107; color: black; }
</style>
""", unsafe_allow_html=True)

# Interface
st.markdown('<h1 class="main-title">⚡ Math Core 3000</h1>', unsafe_allow_html=True)
badge = "badge-cpp" if backend_type == "C++" else "badge-python"
st.markdown(f'<p style="text-align:center"><span class="badge {badge}">{backend_type} Backend</span></p>', unsafe_allow_html=True)

# Calculadora
op = st.selectbox("Operation", ["➕ Addition", "➖ Subtraction", "✖️ Multiplication", 
                                  "➗ Division", "🔢 Power", "√ Square Root", "💯 Percentage"])

col1, col2 = st.columns(2)
with col1:
    n1 = st.number_input("First Number", value=0.0)
with col2:
    n2 = st.number_input("Second Number", value=0.0, disabled=(op=="√ Square Root"))

if st.button("🚀 Calculate", use_container_width=True):
    try:
        ops = {"➕ Addition": "add", "➖ Subtraction": "subtract", 
               "✖️ Multiplication": "multiply", "➗ Division": "divide",
               "🔢 Power": "power", "√ Square Root": "sqrt", "💯 Percentage": "percentage"}
        
        func = getattr(calc, ops[op])
        result = func(n1) if op == "√ Square Root" else func(n1, n2)
        
        st.markdown(f"""
            <div class="result-box">
                <div class="result-number">{result:.6g}</div>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ {e}")

st.markdown(f'<p style="text-align:center; color:#8B8B8B; margin-top:2rem">🚀 Math Core 3000 • {backend_type} Powered</p>', unsafe_allow_html=True)
