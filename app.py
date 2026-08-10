import streamlit as st
import time

# Tenta importar C++, senão usa Python
try:
    import calc_backend
    calc = calc_backend.AdvancedCalculator()
    backend_type = "C++"
    backend_name = "⚡ C++ Engine"
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
    backend_name = "🐍 Quantum Engine"

# Configuração da página
st.set_page_config(page_title="Math Core 3000", page_icon="🧮", layout="centered")

# CSS Elegante com fundo cinza e calculadora arredondada
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #e94560;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 30px rgba(233, 69, 96, 0.3);
        letter-spacing: -1px;
    }
    
    .subtitle {
        color: #a8a8b3;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Calculadora com fundo cinza e bordas arredondadas */
    .calculator-container {
        background: linear-gradient(145deg, #2d2d3f 0%, #252536 100%);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        margin: 0 auto;
        max-width: 550px;
        min-height: 420px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5),
                    0 0 0 1px rgba(255, 255, 255, 0.05),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Display da calculadora */
    .calculator-display {
        background: #1a1a28;
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.8rem;
        text-align: right;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.3);
    }
    
    .calculator-display-text {
        color: #e94560;
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .result-box {
        background: linear-gradient(145deg, rgba(233, 69, 96, 0.08), rgba(233, 69, 96, 0.03));
        border: 2px solid #e94560;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 0 30px rgba(233, 69, 96, 0.1);
    }
    
    .result-number {
        color: #e94560;
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(233, 69, 96, 0.3);
    }
    
    .result-expression {
        color: #8888a0;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #e94560 0%, #c23152 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem;
        width: 100%;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(233, 69, 96, 0.5);
        background: linear-gradient(135deg, #ff6b81 0%, #e94560 100%);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Select box */
    .stSelectbox>div>div {
        background: #1a1a28 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Number inputs */
    .stNumberInput>div>div {
        background: #1a1a28 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stNumberInput>div>div>input {
        color: white !important;
    }
    
    /* Badge */
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
        background: linear-gradient(135deg, #e94560, #c23152);
        color: white;
        box-shadow: 0 2px 10px rgba(233, 69, 96, 0.3);
    }
    
    .badge-python {
        background: linear-gradient(135deg, #0f3460, #16213e);
        color: #e94560;
        border: 1px solid #e94560;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6c6c80;
        margin-top: 2rem;
        font-size: 0.8rem;
        font-family: 'Inter', sans-serif;
    }
    
    .footer span {
        color: #e94560;
    }
    
    /* History */
    .history-item {
        background: rgba(255, 255, 255, 0.03);
        border-left: 3px solid #e94560;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #c0c0d0;
    }
    
    /* Labels */
    label {
        color: #a0a0b0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Interface Principal
st.markdown('<h1 class="main-title">🧮 Math Core 3000</h1>', unsafe_allow_html=True)

# Badge do backend
if backend_type == "C++":
    badge_html = f'<span class="badge badge-cpp">{backend_name}</span>'
else:
    badge_html = f'<span class="badge badge-python">{backend_name}</span>'

st.markdown(f'<p class="subtitle">High-Performance Calculator • {badge_html}</p>', unsafe_allow_html=True)

# Container da Calculadora (fundo cinza, arredondado)
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Display da calculadora
st.markdown("""
    <div class="calculator-display">
        <span class="calculator-display-text">0</span>
    </div>
""", unsafe_allow_html=True)

# Seletor de operação
operations = {
    "➕ Addition (+)": "add",
    "➖ Subtraction (−)": "subtract", 
    "✖️ Multiplication (×)": "multiply",
    "➗ Division (÷)": "divide",
    "🔢 Power (xʸ)": "power",
    "√ Square Root": "sqrt",
    "💯 Percentage (%)": "percentage"
}

selected_op = st.selectbox(
    "Select Operation",
    list(operations.keys()),
    label_visibility="visible"
)

# Inputs
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("First Number", value=0.0, format="%.4f", key="num1")

with col2:
    if operations[selected_op] == "sqrt":
        num2 = 0
        st.number_input("Second Number", value=0.0, disabled=True, key="num2_disabled")
    else:
        num2 = st.number_input("Second Number", value=0.0, format="%.4f", key="num2")

# Botão calcular
if st.button("⚡ Compute", use_container_width=True):
    try:
        operation_func = getattr(calc, operations[selected_op])
        
        if operations[selected_op] == "sqrt":
            result = operation_func(num1)
            expression = f"√({num1})"
        else:
            result = operation_func(num1, num2)
            op_symbol = selected_op.split("(")[1].replace(")", "") if "(" in selected_op else selected_op.split()[1]
            expression = f"{num1} {op_symbol} {num2}"
        
        result_str = f"{result:.6g}"
        
        # Atualizar display
        st.markdown(f"""
            <div class="calculator-display">
                <span class="calculator-display-text">{result_str}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Mostrar resultado estilizado
        st.markdown(f"""
            <div class="result-box">
                <div class="result-number">{result_str}</div>
                <div class="result-expression">{expression} = {result_str}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Salvar no histórico
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        st.session_state.history.append({
            'expression': expression,
            'result': result_str,
            'timestamp': time.strftime("%H:%M:%S")
        })
        
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Histórico
if 'history' in st.session_state and st.session_state.history:
    with st.expander(f"📜 Calculation History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expression']}</strong> = {item['result']}
                    <span style="color: #6c6c80; float: right;">{item['timestamp']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# Footer atualizado
st.markdown("""
    <div class="footer">
        🚀 <span>Math Core 3000</span> • <span>Python & C++</span> Powered
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧮 Math Core 3000")
    st.markdown(f"**Engine:** {backend_name}")
    st.markdown(f"**Total Operations:** {len(st.session_state.get('history', []))}")
    st.markdown("---")
    st.markdown("**Available Operations:**")
    st.markdown("➕ ➖ ✖️ ➗")
    st.markdown("🔢 √ 💯")
    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- 🐍 Python 3.10+")
    st.markdown("- ⚡ C++17 (Pybind11)")
    st.markdown("- 🎨 Streamlit")
