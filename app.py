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

# CSS Elegante com fundo cinza, bordas arredondadas e sombras
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
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(108, 99, 255, 0.3);
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #8B8B8B;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Calculadora com fundo cinza, bordas arredondadas e sombra */
    .calculator-container {
        background: #2C2C2E;
        border-radius: 24px;
        padding: 2.5rem 2rem;
        margin: 0 auto;
        max-width: 500px;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 8px 20px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .result-display {
        background: #1C1C1E;
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .result-number {
        font-family: 'JetBrains Mono', monospace;
        color: #6C63FF;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 0 15px rgba(108, 99, 255, 0.3);
    }
    
    .result-label {
        color: #8B8B8B;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #4834D4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        width: 100%;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(108, 99, 255, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .stSelectbox > div > div {
        background: #1C1C1E !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stNumberInput > div > div {
        background: #1C1C1E !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stNumberInput input {
        color: white !important;
    }
    
    .history-item {
        background: rgba(108, 99, 255, 0.05);
        border-left: 3px solid #6C63FF;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    .footer {
        text-align: center;
        color: #8B8B8B;
        margin-top: 2rem;
        font-size: 0.85rem;
        font-family: 'Inter', sans-serif;
    }
    
    .badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    .badge-cpp {
        background: linear-gradient(135deg, #6C63FF, #4834D4);
        color: white;
    }
    
    .badge-python {
        background: linear-gradient(135deg, #3776AB, #FFD43B);
        color: white;
    }
    
    .badge-hybrid {
        background: linear-gradient(135deg, #6C63FF, #3776AB);
        color: white;
    }
    
    .stExpander {
        background: #2C2C2E;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    label {
        color: #8B8B8B !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Interface
st.markdown('<h1 class="main-title">⚡ Math Core 3000</h1>', unsafe_allow_html=True)

# Badge híbrido elegante
st.markdown(f'<p class="subtitle">Advanced Calculation Engine • <span class="badge badge-hybrid">Python & C++</span></p>', unsafe_allow_html=True)

# Calculator Container
with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
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
        "Select Operation",
        list(operations.keys()),
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        num1 = st.number_input("First Number", value=0.0, format="%.4f")
    
    with col2:
        if operations[selected_op] == "sqrt":
            num2 = 0
            st.number_input("Second Number", value=0.0, disabled=True)
        else:
            num2 = st.number_input("Second Number", value=0.0, format="%.4f")
    
    if st.button("🚀 Calculate", use_container_width=True):
        try:
            operation_func = getattr(calc, operations[selected_op])
            
            if operations[selected_op] == "sqrt":
                result = operation_func(num1)
                expression = f"√({num1})"
            else:
                result = operation_func(num1, num2)
                expression = f"{num1} {selected_op.split()[1]} {num2}"
            
            result_str = f"{result:.6g}"
            
            st.markdown(f"""
                <div class="result-display">
                    <div class="result-label">Result</div>
                    <div class="result-number">{result_str}</div>
                    <div style="color: #6B6B6B; font-size: 0.8rem; margin-top: 0.5rem;">
                        {expression} = {result_str}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.session_state.history.append({
                'expression': expression,
                'result': result_str,
                'timestamp': time.strftime("%H:%M:%S")
            })
            
        except Exception as e:
            st.error(f"⚠️ {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# History
if st.session_state.history:
    with st.expander(f"📜 Calculation History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expression']}</strong> = {item['result']}
                    <span style="color: #8B8B8B; float: right;">{item['timestamp']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# Footer
st.markdown(f"""
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
    st.markdown("➕ Addition")
    st.markdown("➖ Subtraction")
    st.markdown("✖️ Multiplication")
    st.markdown("➗ Division")
    st.markdown("🔢 Power")
    st.markdown("√ Square Root")
    st.markdown("💯 Percentage")
    st.markdown("---")
    st.markdown("[📦 GitHub Repository](https://github.com/seu-usuario/math-core-3000)")
