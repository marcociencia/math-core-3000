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
    
    /* Botão Calculate */
    div[data-testid="stButton"] > button:first-of-type {
        background-color: #5C4FFF !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 12px !important;
        margin-top: 10px !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stButton"] > button:first-of-type:hover {
        background-color: #4B3BE0 !important;
        box-shadow: 0 5px 15px rgba(92, 79, 255, 0.4) !important;
        transform: translateY(-2px);
    }
    
    div[data-testid="stButton"] > button p {
        font-size: 0.95rem !important;
        color: white !important;
    }
    
    /* Botão Reset (segundo botão) */
    div[data-testid="stButton"] > button:nth-of-type(2),
    .reset-btn button {
        background-color: #FF5252 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 10px !important;
        margin-top: 8px !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stButton"] > button:nth-of-type(2):hover,
    .reset-btn button:hover {
        background-color: #E04848 !important;
        box-shadow: 0 5px 15px rgba(255, 82, 82, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Display de resultado */
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
    
    /* Histórico */
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

# Session state
if 'display_value' not in st.session_state:
    st.session_state.display_value = "0"
if 'display_expr' not in st.session_state:
    st.session_state.display_expr = "Enter a calculation"
if 'last_result' not in st.session_state:
    st.session_state.last_result = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'n1' not in st.session_state:
    st.session_state.n1 = 9.00
if 'n2' not in st.session_state:
    st.session_state.n2 = 0.00
if 'selected_op' not in st.session_state:
    st.session_state.selected_op = "➕ Addition"

# Cabeçalho da Calculadora
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

# Operações com símbolos
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

# Callback para quando a operação mudar
def on_op_change():
    st.session_state.selected_op = st.session_state.op_selector
    # Se for operação de um número só, usa last_result como n1
    if st.session_state.selected_op in ["√ Square Root", "∛ Cube Root"]:
        st.session_state.n1 = float(st.session_state.last_result)

# Callback para reset
def reset_all():
    st.session_state.display_value = "0"
    st.session_state.display_expr = "Enter a calculation"
    st.session_state.last_result = 0.0
    st.session_state.n1 = 0.00
    st.session_state.n2 = 0.00
    st.session_state.history = []
    st.session_state.selected_op = "➕ Addition"

selected_op = st.selectbox(
    "Operation", 
    op_names, 
    label_visibility="visible",
    key="op_selector",
    on_change=on_op_change
)

# Determina se é operação de um número só
is_single = selected_op in ["√ Square Root", "∛ Cube Root"]

# Inputs lado a lado
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input(
        "First Number", 
        value=float(st.session_state.last_result) if is_single else st.session_state.n1,
        format="%.2f", 
        key="n1"
    )

with col2:
    if is_single:
        num2 = st.number_input(
            "Second Number", 
            value=0.00, 
            format="%.2f", 
            disabled=True, 
            key="n2"
        )
    else:
        num2 = st.number_input(
            "Second Number", 
            value=st.session_state.n2,
            format="%.2f", 
            key="n2"
        )

# Botões Calculate e Reset lado a lado
col_calc, col_reset = st.columns([3, 1])

with col_calc:
    if st.button("🚀 Calculate", use_container_width=True, key="calc_btn"):
        try:
            op_func = getattr(calc, operations[selected_op])
            
            if is_single:
                result = op_func(num1)
                if selected_op == "√ Square Root":
                    expr = f"√({num1})"
                else:
                    expr = f"∛({num1})"
            else:
                result = op_func(num1, num2)
                # Pega só o símbolo da operação
                symbol = selected_op.split()[0]
                expr = f"{num1} {symbol} {num2}"
            
            result_str = f"{result:.6g}" if result != int(result) else str(int(result))
            
            # Atualiza session state
            st.session_state.display_value = result_str
            st.session_state.display_expr = f"{expr} = {result_str}"
            st.session_state.last_result = result
            st.session_state.n1 = num1
            st.session_state.n2 = num2
            
            # Adiciona ao histórico
            st.session_state.history.append({
                'expr': expr,
                'result': result_str,
                'time': time.strftime("%H:%M")
            })
            
        except Exception as e:
            st.session_state.display_value = "Error"
            st.error(f"Error: {str(e)}")

with col_reset:
    if st.button("🔄 Reset", use_container_width=True, key="reset_btn", on_click=reset_all):
        pass

# Display do Resultado
st.markdown(f"""
    <div class="display-box">
        <div class="display-expression">{st.session_state.display_expr}</div>
        <div class="display-result">{st.session_state.display_value}</div>
    </div>
""", unsafe_allow_html=True)

# Histórico
if st.session_state.history:
    with st.expander(f"📜 History ({len(st.session_state.history)})", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expr']}</strong> = {item['result']}
                    <span style="color:#8E8E93;float:right;font-size:0.7rem;">{item['time']}</span>
                </div>
            """, unsafe_allow_html=True)

# Rodapé
st.markdown("""
    <div style="text-align: center; color: #6E707E; font-size: 0.75rem; margin-top: 25px; font-family: 'Inter', sans-serif;">
        🚀 Math Core 3000 • Python & C++ Powered
    </div>
""", unsafe_allow_html=True)
