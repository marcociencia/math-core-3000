import streamlit as st
import time

if "n2_input" not in st.session_state:
    st.session_state["n2_input"] = 0.0
    
# Try import C++, otherwise, use Python
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
        def cbrt(self, a):
            if a < 0: return -((-a) ** (1/3))
            return a ** (1/3)
        def percentage(self, a, b): return (a * b) / 100.0
    
    calc = PythonCalc()
    backend_type = "Python"

st.set_page_config(page_title="Math Core 3000", page_icon="⚡", layout="centered")

# CSS Estilizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    [data-testid="stAppViewContainer"] {
        background-color: #9E9E9E !important; 
    }
    
    [data-testid="stMainBlockContainer"], .block-container {
        background-color: #1A1C24 !important;
        border-radius: 16px !important;
        padding: 40px 40px 30px 40px !important;
        max-width: 600px !important;
        margin-top: 8vh !important;
        margin-bottom: 8vh !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    label, .st-emotion-cache-1yvjcxv p, .st-emotion-cache-16idsys p {
        color: #A0A0A5 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin-bottom: 2px !important;
    }
    
    div[data-baseweb="select"] > div,
    input[type="number"] {
        background-color: #282A36 !important;
        border: 1px solid #363845 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 8px 12px !important;
    }
    
    div[data-baseweb="select"] > div:focus-within,
    input[type="number"]:focus {
        border-color: #5C4FFF !important;
        box-shadow: 0 0 0 1px #5C4FFF !important;
    }
    
    input[type="number"]::-webkit-inner-spin-button, 
    input[type="number"]::-webkit-outer-spin-button { 
        -webkit-appearance: none; 
        margin: 0; 
    }
    
    div[data-testid="stButton"] > button {
        transition: all 0.3s ease;
    }
    
    div[data-testid="stButton"] > button p {
        font-size: 0.95rem !important;
    }
    
    .display-box {
        border: 2px solid #5C4FFF;
        border-radius: 12px;
        background-color: #1A1C24;
        text-align: center;
        padding: 25px;
        margin-top: 15px;
    }
    
    .display-expression {
        color: #8E8E93;
        font-size: 0.85rem;
        font-family: 'Inter', sans-serif;
        margin-bottom: 5px;
    }
    
    .display-result {
        color: #8C82FF;
        font-size: 2.8rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    
    .history-item {
        background: #282A36;
        border-left: 3px solid #5C4FFF;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: #CCCCCC;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Start of Session State
# ============================================
if 'display_value' not in st.session_state:
    st.session_state.display_value = "0"
if 'display_expr' not in st.session_state:
    st.session_state.display_expr = "Enter a calculation"
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_op' not in st.session_state:
    st.session_state.current_op = "➕ Addition"
if 'n1_input' not in st.session_state:
    st.session_state.n1_input = 0.0
if 'n2_input' not in st.session_state:
    st.session_state.n2_input = 0.0
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = ""

# ============================================
# Mapping de Operações
# ============================================
operations = {
    "➕ Addition": "add",
    "➖ Subtraction": "subtract", 
    "✖️ Multiplication": "multiply",
    "➗ Division": "divide",
    "🔢 Power (xʸ)": "power",
    "√ Square Root": "sqrt",
    "∛ Cube Root": "cbrt",
    "💯 Percentage": "percentage"
}
op_names = list(operations.keys())

# ============================================
# Functions of Callbacks
# ============================================
def reset_all():
    """Callback para resetar tudo com segurança"""
    st.session_state.display_value = "0"
    st.session_state.display_expr = "Enter a calculation"
    st.session_state.last_result = None
    st.session_state.history = []
    st.session_state.current_op = "➕ Addition"
    st.session_state.n1_input = 0.0
    st.session_state.n2_input = 0.0
    st.session_state.error_msg = ""

def on_op_change():
    """Callback acionado ANTES de a tela recarregar ao mudar operação"""
    st.session_state.current_op = st.session_state.op_selector
    # Mantém o último resultado (se houver) no n1_input ao mudar de operação
    if st.session_state.last_result is not None:
        st.session_state.n1_input = float(st.session_state.last_result)

def do_calculation():
    """Callback principal que realiza o cálculo e atualiza os inputs"""
    st.session_state.error_msg = ""
    try:
        selected_op = st.session_state.op_selector
        op_func = getattr(calc, operations[selected_op])
        
        # Puxa os valores diretamente do session_state
        n1 = st.session_state.n1_input
        n2 = st.session_state.n2_input
        is_single = selected_op in ["√ Square Root", "∛ Cube Root"]
        
        if is_single:
            result = op_func(n1)
            expr = f"√({n1})" if selected_op == "√ Square Root" else f"∛({n1})"
        else:
            result = op_func(n1, n2)
            symbol = selected_op.split()[0]
            expr = f"{n1} {symbol} {n2}"
        
        # Formata resultado (remove zeros irrelevantes)
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = f"{result:.6g}"
        
        # Atualiza a interface
        st.session_state.display_value = result_str
        st.session_state.display_expr = f"{expr} = {result_str}"
        st.session_state.last_result = float(result)
        
        # ===== CORREÇÃO DEFINITIVA =====
        # Aqui, como estamos dentro de um callback (antes da tela desenhar), 
        # atualizar n1_input é perfeitamente seguro e não gera erros.
        st.session_state.n1_input = float(result)
        
        # Adiciona ao histórico
        st.session_state.history.append({
            'expr': expr,
            'result': result_str,
            'time': time.strftime("%H:%M")
        })
        
    except Exception as e:
        st.session_state.error_msg = str(e)

# ============================================
# Interface Visual (Header)
# ============================================
st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: white; font-family: 'Inter', sans-serif; font-size: 2.2rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px;">
            <span style="color: #FF7043;">⚡</span> Math Core 3000
        </h1>
        <div>
            <span style="background-color: #FFC107; color: #000; padding: 4px 16px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; font-family: 'Inter', sans-serif;">
                Python & C++ Backend
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ============================================
# Inputs de Operação e Números
# ============================================
op_index = op_names.index(st.session_state.current_op) if st.session_state.current_op in op_names else 0

selected_op = st.selectbox(
    "Operation", 
    op_names, 
    index=op_index,
    label_visibility="visible",
    key="op_selector",
    on_change=on_op_change  # Aciona callback na mudança
)

is_single = selected_op in ["√ Square Root", "∛ Cube Root"]

col1, col2 = st.columns(2)

with col1:
    # Apenas passa a key; o valor será puxado do session state atual
    st.number_input("First Number", format="%.2f", key="n1_input")

with col2:
    if is_single:
        # Se desabilitado, criamos um campo genérico de valor 0.0
        st.number_input("Second Number", value=0.00, format="%.2f", disabled=True, key="n2_disabled")
    else:
        st.number_input("Second Number", format="%.2f", key="n2_input")

# ============================================
# Buttons com Callbacks
# ============================================
col_calc, col_reset = st.columns([3, 1])

with col_calc:
    # Vinculamos o cálculo ao on_click, evitando usar o 'if st.button:'
    st.button("🚀 Calculate", use_container_width=True, key="calc_btn", on_click=do_calculation)

with col_reset:
    st.button("🔄 Reset", use_container_width=True, key="reset_btn", on_click=reset_all)

# ============================================
# Alertas e Display Final
# ============================================
if st.session_state.error_msg:
    st.error(f"Error: {st.session_state.error_msg}")

st.markdown(f"""
    <div class="display-box">
        <div class="display-expression">{st.session_state.display_expr}</div>
        <div class="display-result">{st.session_state.display_value}</div>
    </div>
""", unsafe_allow_html=True)

# ============================================
# History & Footer
# ============================================
if st.session_state.history:
    with st.expander(f"📜 History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expr']}</strong> = {item['result']}
                    <span style="color:#8E8E93;float:right;font-size:0.7rem;">{item['time']}</span>
                </div>
            """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; color: #6E707E; font-size: 0.75rem; margin-top: 25px; font-family: 'Inter', sans-serif;">
        🚀 Math Core 3000 • Python & C++ Powered
    </div>
""", unsafe_allow_html=True)
