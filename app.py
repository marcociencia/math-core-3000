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
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1A1B23 100%);
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #6C63FF;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 30px rgba(108, 99, 255, 0.3);
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: #8B8B8B;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Container da Calculadora - Fundo Cinza e Bordas Arredondadas */
    .calculator-wrapper {
        background: #1E1E2E;
        border-radius: 24px;
        padding: 2.5rem 2rem;
        max-width: 550px;
        margin: 0 auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.15);
    }
    
    .calculator-wrapper .stSelectbox > div > div {
        background: #2A2A3E !important;
        border: 1px solid rgba(108, 99, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        color: white !important;
    }
    
    .calculator-wrapper .stNumberInput > div > div {
        background: #2A2A3E !important;
        border: 1px solid rgba(108, 99, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        color: white !important;
    }
    
    .calculator-wrapper label {
        color: #B0B0C0 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .result-box {
        background: rgba(108, 99, 255, 0.08);
        border: 2px solid #6C63FF;
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        margin: 1.8rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 15px rgba(108, 99, 255, 0.15); }
        to { box-shadow: 0 0 35px rgba(108, 99, 255, 0.35); }
    }
    
    .result-label {
        color: #8B8B8B;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    .result-number {
        font-family: 'JetBrains Mono', monospace;
        color: #6C63FF;
        font-size: 2.8rem;
        font-weight: 700;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #4834D4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif !important;
        margin-top: 0.5rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(108, 99, 255, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    .badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    
    .badge-cpp {
        background: linear-gradient(135deg, #6C63FF, #4834D4);
        color: white;
    }
    
    .badge-python {
        background: linear-gradient(135deg, #FFC107, #FF9800);
        color: #1A1B23;
    }
    
    .footer-text {
        text-align: center;
        color: #6B6B80;
        margin-top: 2.5rem;
        font-size: 0.85rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .footer-text span {
        color: #6C63FF;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Interface
st.markdown('<h1 class="main-title">⚡ Math Core 3000</h1>', unsafe_allow_html=True)

# Badge do backend
badge = "badge-cpp" if backend_type == "C++" else "badge-python"
badge_text = "⚡ C++ Engine" if backend_type == "C++" else "🐍 Python Engine"
st.markdown(f'<p class="subtitle"><span class="badge {badge}">{badge_text}</span></p>', unsafe_allow_html=True)

# Container da Calculadora
st.markdown('<div class="calculator-wrapper">', unsafe_allow_html=True)

op = st.selectbox(
    "Select Operation",
    ["➕ Addition", "➖ Subtraction", "✖️ Multiplication", 
     "➗ Division", "🔢 Power", "√ Square Root", "💯 Percentage"]
)

col1, col2 = st.columns(2)
with col1:
    n1 = st.number_input("First Number", value=0.0, format="%.4f")
with col2:
    n2 = st.number_input("Second Number", value=0.0, format="%.4f", disabled=(op=="√ Square Root"))

if st.button("Calculate", use_container_width=True):
    try:
        ops = {
            "➕ Addition": "add", "➖ Subtraction": "subtract", 
            "✖️ Multiplication": "multiply", "➗ Division": "divide",
            "🔢 Power": "power", "√ Square Root": "sqrt", "💯 Percentage": "percentage"
        }
        
        func = getattr(calc, ops[op])
        result = func(n1) if op == "√ Square Root" else func(n1, n2)
        
        # Formata o resultado
        if isinstance(result, float):
            if abs(result) > 1e10 or (abs(result) < 1e-10 and result != 0):
                result_str = f"{result:.6e}"
            else:
                result_str = f"{result:.10f}".rstrip('0').rstrip('.')
        else:
            result_str = str(result)
        
        st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Result</div>
                <div class="result-number">{result_str}</div>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"⚠️ {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <p class="footer-text">
        🚀 Math Core 3000 • <span>Python & C++ Powered</span>
    </p>
""", unsafe_allow_html=True)
