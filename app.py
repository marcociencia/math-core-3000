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

# CSS - Layout Horizontal
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
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 20px rgba(108, 99, 255, 0.3);
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #8B8B8B;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Calculadora */
    .calculator-container {
        background: #2C2C2E;
        border-radius: 20px;
        padding: 25px 25px 20px 25px;
        max-width: 480px;
        margin: 0 auto;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 8px 20px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* Display */
    .display {
        background: #1C1C1E;
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
        text-align: right;
        min-height: 100px;
    }
    
    .display-label {
        color: #6B6B6B;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Inter', sans-serif;
        margin-bottom: 5px;
    }
    
    .display-result {
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.1;
        word-break: break-all;
    }
    
    .display-expression {
        color: #6B6B6B;
        font-size: 0.85rem;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 5px;
    }
    
    /* Selectbox */
    .stSelectbox [data-baseweb="select"] {
        background: #1C1C1E !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: white !important;
    }
    
    /* Inputs */
    .stNumberInput [data-baseweb="input"] {
        background: #1C1C1E !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    .stNumberInput input {
        color: white !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Botão */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #4834D4 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        width: 100% !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
        margin-top: 5px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(108, 99, 255, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Labels */
    label {
        color: #8B8B8B !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* History */
    .history-item {
        background: rgba(108, 99, 255, 0.05);
        border-left: 3px solid #6C63FF;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #CCCCCC;
    }
    
    .history-time {
        color: #8B8B8B;
        font-size: 0.7rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6B6B6B;
        margin-top: 2rem;
        font-size: 0.8rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    .badge-hybrid {
        background: linear-gradient(135deg, #6C63FF, #3776AB);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #2C2C2E;
        border-radius: 12px;
    }
    
    /* Espaçamento */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Colunas */
    [data-testid="column"] {
        padding: 0 5px;
    }
    
    /* Remover espaço do st.error */
    .stAlert {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'display_result' not in st.session_state:
    st.session_state.display_result = "0"
if 'display_expression' not in st.session_state:
    st.session_state.display_expression = "Enter a calculation"

# Interface
st.markdown('<h1 class="main-title">⚡ Math Core 3000</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">Advanced Calculation Engine • <span class="badge badge-hybrid">Python & C++</span></p>', unsafe_allow_html=True)

# Calculadora
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Display
st.markdown(f"""
    <div class="display">
        <div class="display-label">Result</div>
        <div class="display-result">{st.session_state.display_result}</div>
        <div class="display-expression">{st.session_state.display_expression}</div>
    </div>
""", unsafe_allow_html=True)

# Operações
operations = {
    "➕ Addition": "add",
    "➖ Subtraction": "subtract", 
    "✖️ Multiplication": "multiply",
    "➗ Division": "divide",
    "🔢 Power": "power",
    "√ Square Root": "sqrt",
    "💯 Percentage": "percentage"
}

selected_op = st.selectbox(
    "Operation",
    list(operations.keys()),
    label_visibility="visible"
)

# Inputs lado a lado
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("First Number", value=0.0, format="%.2f", key="num1")

with col2:
    if operations[selected_op] == "sqrt":
        num2 = 0
        st.number_input("Second Number", value=0.0, disabled=True, key="num2_disabled")
    else:
        num2 = st.number_input("Second Number", value=0.0, format="%.2f", key="num2")

# Botão Calculate
calculate_clicked = st.button("Calculate", use_container_width=True)

if calculate_clicked:
    try:
        operation_func = getattr(calc, operations[selected_op])
        
        if operations[selected_op] == "sqrt":
            result = operation_func(num1)
            expression = f"√({num1})"
        else:
            result = operation_func(num1, num2)
            op_symbol = selected_op.split()[1]
            expression = f"{num1} {op_symbol} {num2}"
        
        result_str = f"{result:.6g}"
        
        # Atualizar display
        st.session_state.display_result = result_str
        st.session_state.display_expression = f"{expression} = {result_str}"
        
        # Adicionar ao histórico
        st.session_state.history.append({
            'expression': expression,
            'result': result_str,
            'timestamp': time.strftime("%H:%M:%S")
        })
        
        # Mostrar resultado (sem rerun)
        st.success(f"✅ Calculated: {expression} = {result_str}")
        
    except Exception as e:
        st.error(f"⚠️ {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# History
if st.session_state.history:
    st.markdown('<br>', unsafe_allow_html=True)
    with st.expander(f"📜 Calculation History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expression']}</strong> = {item['result']}
                    <span class="history-time" style="float: right;">{item['timestamp']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", use_container_width=True, key="clear_history"):
            st.session_state.history = []
            st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        🚀 Math Core 3000 v1.0.0 • Python & C++ Powered
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧮 Math Core 3000")
    st.markdown(f"**Engine:** Python & C++")
    st.markdown(f"**Total Operations:** {len(st.session_state.history)}")
    st.markdown("---")
    st.markdown("**Available Operations:**")
    st.markdown("➕ ➖ ✖️ ➗")
    st.markdown("🔢 √ 💯")
    st.markdown("---")
    st.markdown("[📦 GitHub Repository](https://github.com/seu-usuario/math-core-3000)")
    st.markdown("---")
    st.markdown(f"🔗 [Live Demo](https://math-core-3000-jwdvud23nqkr28jezsgura.streamlit.app/)")
