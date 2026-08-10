import streamlit as st
import subprocess
import sys
import os
import time

# Page configuration
st.set_page_config(
    page_title="Math Core 3000",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# COMPILAÇÃO AUTOMÁTICA DO C++
# ============================================
@st.cache_resource
def get_calculator():
    """Compila e carrega o módulo C++ automaticamente"""
    try:
        import calc_backend
        st.success("⚡ C++ Backend Ativado!")
        return calc_backend.AdvancedCalculator(), "C++"
    except ImportError:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Passo 1: Instalar compilador
            status_text.info("📦 Instalando compilador C++...")
            progress_bar.progress(25)
            
            os.system("apt-get update -qq > /dev/null 2>&1")
            os.system("apt-get install -y -qq build-essential g++ python3-dev > /dev/null 2>&1")
            
            # Passo 2: Instalar pybind11
            status_text.info("📦 Instalando pybind11...")
            progress_bar.progress(50)
            
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", "pybind11>=2.10.0"]
            )
            
            # Passo 3: Compilar
            status_text.info("🔨 Compilando módulo C++...")
            progress_bar.progress(75)
            
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", "-e", "."]
            )
            
            # Passo 4: Verificar
            import calc_backend
            progress_bar.progress(100)
            status_text.success("✅ C++ Backend compilado com sucesso!")
            
            return calc_backend.AdvancedCalculator(), "C++"
            
        except Exception as e:
            progress_bar.empty()
            status_text.warning(f"⚠️ Usando Python (C++ não compilou)")
            return PythonCalculator(), "Python"

class PythonCalculator:
    """Calculadora Python de backup"""
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0: raise ZeroDivisionError("Division by zero!")
        return a / b
    def power(self, a, b): return a ** b
    def sqrt(self, a):
        if a < 0: raise ValueError("Cannot calculate square root of negative number!")
        return a ** 0.5
    def percentage(self, a, b): return (a * b) / 100.0

# Inicializa a calculadora
calc, backend_type = get_calculator()

# ============================================
# INTERFACE ELEGANTE
# ============================================

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1A1B23 100%);
    }
    
    .main-title {
        font-family: 'JetBrains Mono', monospace;
        color: #6C63FF;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(108, 99, 255, 0.3);
    }
    
    .subtitle {
        color: #8B8B8B;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .calculator-container {
        background: rgba(38, 39, 48, 0.8);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.2);
    }
    
    .result-display {
        background: rgba(108, 99, 255, 0.1);
        border: 2px solid #6C63FF;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(108, 99, 255, 0.2); }
        to { box-shadow: 0 0 30px rgba(108, 99, 255, 0.4); }
    }
    
    .result-number {
        font-family: 'JetBrains Mono', monospace;
        color: #6C63FF;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #4834D4 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(108, 99, 255, 0.4);
    }
    
    .history-item {
        background: rgba(108, 99, 255, 0.05);
        border-left: 3px solid #6C63FF;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    .footer {
        text-align: center;
        color: #8B8B8B;
        margin-top: 2rem;
        font-size: 0.8rem;
    }
    
    .badge-cpp {
        background: linear-gradient(135deg, #6C63FF, #4834D4);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .badge-python {
        background: linear-gradient(135deg, #FFC107, #FF9800);
        color: black;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Main Interface
st.markdown('<h1 class="main-title">⚡ Math Core 3000</h1>', unsafe_allow_html=True)

# Backend badge
if backend_type == "C++":
    badge_html = '<span class="badge-cpp">⚡ C++ Backend</span>'
else:
    badge_html = '<span class="badge-python">🐍 Python Backend</span>'

st.markdown(f'<p class="subtitle">Advanced Calculator • {badge_html}</p>', unsafe_allow_html=True)

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
                    <div class="result-number">{result_str}</div>
                    <div style="color: #8B8B8B; margin-top: 0.5rem;">
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
    with st.expander(f"📜 History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expression']}</strong> = {item['result']}
                    <span style="color: #8B8B8B; float: right;">{item['timestamp']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()

st.markdown(f"""
    <div class="footer">
        🚀 Math Core 3000 v1.0.0 • {backend_type} Powered
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧮 About")
    st.markdown(f"**Backend:** {backend_type}")
    st.markdown(f"**Operations:** {len(st.session_state.history)}")
    st.markdown("---")
    st.markdown("**Operations:**")
    st.markdown("➕ ➖ ✖️ ➗ 🔢 √ 💯")
