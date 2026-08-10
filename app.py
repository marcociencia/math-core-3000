import streamlit as st
import time

# Tenta importar C++, senão usa Python
try:
    import calc_backend
    calc = calc_backend.AdvancedCalculator()
    backend_type = "C++"
except:
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

st.set_page_config(page_title="Math Core 3000", page_icon="🧮", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Fundo geral */
    .stApp {
        background: #1C1C1E;
    }
    
    /* Container principal do Streamlit */
    .block-container {
        padding: 1rem 1rem 0.5rem 1rem !important;
        max-width: 750px !important;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF;
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #8E8E93;
        text-align: center;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* ========== CALCULADORA ========== */
    .calculator-container {
        background: #3A3A3C;
        border-radius: 16px;
        padding: 20px 24px 24px 24px;
        margin: 0 auto;
        width: 100%;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.6),
            0 0 0 1px rgba(255, 255, 255, 0.05) inset;
    }
    
    /* Display */
    .display {
        background: #2C2C2E;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        text-align: right;
        min-height: 70px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .display-label {
        color: #8E8E93;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'Inter', sans-serif;
        margin-bottom: 2px;
    }
    
    .display-value {
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
        word-break: break-all;
    }
    
    .display-expression {
        color: #8E8E93;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 2px;
    }
    
    /* Select box */
    .stSelectbox [data-baseweb="select"] {
        background: #2C2C2E !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: #FFFFFF !important;
    }
    
    /* Inputs */
    .stNumberInput input {
        background: #2C2C2E !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        padding: 10px 12px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1rem !important;
    }
    
    /* Botão Calculate */
    .stButton > button {
        background: #6C63FF !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.2s ease !important;
        margin-top: 4px !important;
    }
    
    .stButton > button:hover {
        background: #5A52E0 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
    }
    
    /* Labels */
    .stSelectbox label, .stNumberInput label {
        color: #8E8E93 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Remover "Press Enter" */
    .stNumberInput p {
        display: none;
    }
    
    /* History */
    .history-item {
        background: #2C2C2E;
        border-left: 3px solid #6C63FF;
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #CCCCCC;
    }
    
    .footer {
        text-align: center;
        color: #8E8E93;
        margin-top: 1.5rem;
        font-size: 0.78rem;
        font-family: 'Inter', sans-serif;
    }
    
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 14px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        background: rgba(108, 99, 255, 0.2);
        color: #6C63FF;
        border: 1px solid rgba(108, 99, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'display_value' not in st.session_state:
    st.session_state.display_value = "0"
if 'display_expr' not in st.session_state:
    st.session_state.display_expr = "Enter a calculation"

# Interface
st.markdown('<h1 class="main-title">Math Core 3000</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">Advanced Calculation Engine &nbsp; <span class="badge">Python & C++</span></p>', unsafe_allow_html=True)

# CALCULADORA
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Display
st.markdown(f"""
    <div class="display">
        <div class="display-label">Result</div>
        <div class="display-value">{st.session_state.display_value}</div>
        <div class="display-expression">{st.session_state.display_expr}</div>
    </div>
""", unsafe_allow_html=True)

# Operação
operations = {
    "Addition": "add",
    "Subtraction": "subtract", 
    "Multiplication": "multiply",
    "Division": "divide",
    "Power": "power",
    "Square Root": "sqrt",
    "Percentage": "percentage"
}

op_names = list(operations.keys())
selected_op = st.selectbox("Operation", op_names, label_visibility="visible")

# Inputs lado a lado
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("First Number", value=0.0, format="%.2f", key="n1")

with col2:
    if selected_op == "Square Root":
        num2 = 0
        st.number_input("Second Number", value=0.0, disabled=True, key="n2")
    else:
        num2 = st.number_input("Second Number", value=0.0, format="%.2f", key="n2")

# Botão
if st.button("Calculate", use_container_width=True, key="calc_btn"):
    try:
        op_func = getattr(calc, operations[selected_op])
        
        if selected_op == "Square Root":
            result = op_func(num1)
            expr = f"√({num1})"
        else:
            result = op_func(num1, num2)
            expr = f"{num1} {selected_op.lower()} {num2}"
        
        result_str = f"{result:.6g}"
        
        st.session_state.display_value = result_str
        st.session_state.display_expr = f"{expr} = {result_str}"
        
        st.session_state.history.append({
            'expr': expr,
            'result': result_str,
            'time': time.strftime("%H:%M")
        })
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# History
if st.session_state.history:
    with st.expander(f"History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expr']}</strong> = {item['result']}
                    <span style="color:#8E8E93;float:right;font-size:0.7rem;">{item['time']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

st.markdown('<div class="footer">🚀 Math Core 3000 v1.0.0 • Python & C++ Powered</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧮 Math Core 3000")
    st.markdown(f"**Engine:** Python & C++")
    st.markdown(f"**Operations:** {len(st.session_state.history)}")
    st.markdown("---")
    st.markdown("**Available:**")
    st.markdown("➕ ➖ ✖️ ➗ 🔢 √ 💯")
    st.markdown("---")
    st.markdown("[📦 GitHub](https://github.com/seu-usuario/math-core-3000)")
    st.markdown("[🔗 Live Demo](https://math-core-3000-jwdvud23nqkr28jezsgura.streamlit.app/)")
