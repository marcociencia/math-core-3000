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

st.set_page_config(page_title="Math Core 3000", page_icon="⚡", layout="centered")

# CSS Estilizado inspirado na imagem
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Esconde elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fundo geral cinza */
    [data-testid="stAppViewContainer"] {
        background-color: #9E9E9E !important; 
    }
    
    /* Container principal da Calculadora (azul escuro, bordas arredondadas e sombra) */
    [data-testid="stMainBlockContainer"], .block-container {
        background-color: #1A1C24 !important;
        border-radius: 16px !important;
        padding: 40px 40px 30px 40px !important;
        max-width: 600px !important;
        margin-top: 8vh !important;
        margin-bottom: 8vh !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Labels */
    label, .st-emotion-cache-1yvjcxv p, .st-emotion-cache-16idsys p {
        color: #A0A0A5 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin-bottom: 2px !important;
    }
    
    /* Inputs e Selectbox */
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
    
    /* Foco nos inputs */
    div[data-baseweb="select"] > div:focus-within,
    input[type="number"]:focus {
        border-color: #5C4FFF !important;
        box-shadow: 0 0 0 1px #5C4FFF !important;
    }
    
    /* Remover setas dos inputs numéricos */
    input[type="number"]::-webkit-inner-spin-button, 
    input[type="number"]::-webkit-outer-spin-button { 
        -webkit-appearance: none; 
        margin: 0; 
    }
    
    /* Botão Calculate */
    div[data-testid="stButton"] > button {
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
    
    div[data-testid="stButton"] > button:hover {
        background-color: #4B3BE0 !important;
        box-shadow: 0 5px 15px rgba(92, 79, 255, 0.4) !important;
        transform: translateY(-2px);
    }
    
    div[data-testid="stButton"] > button p {
        font-size: 0.95rem !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'display_value' not in st.session_state:
    st.session_state.display_value = "3"

# Cabeçalho da Calculadora
st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: white; font-family: 'Inter', sans-serif; font-size: 2.2rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; justify-content: center; gap: 10px;">
            <span style="color: #FF7043;">⚡</span> Math Core 3000
        </h1>
        <div>
            <span style="background-color: #FFC107; color: #000; padding: 4px 16px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; font-family: 'Inter', sans-serif;">
                Python C++ Backend
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Operações
operations = {
    "√ Square Root": "sqrt",
    "Addition": "add",
    "Subtraction": "subtract", 
    "Multiplication": "multiply",
    "Division": "divide",
    "Power": "power",
    "Percentage": "percentage"
}

op_names = list(operations.keys())
selected_op = st.selectbox("Operation", op_names, label_visibility="visible")

# Inputs lado a lado
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("First Number", value=9.00, format="%.2f", key="n1")

with col2:
    is_sqrt = (selected_op == "√ Square Root")
    num2 = st.number_input("Second Number", value=0.00, format="%.2f", disabled=is_sqrt, key="n2")

# Botão de Calcular
if st.button("🚀 Calculate", use_container_width=True, key="calc_btn"):
    try:
        op_func = getattr(calc, operations[selected_op])
        
        if is_sqrt:
            result = op_func(num1)
        else:
            result = op_func(num1, num2)
        
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = f"{result:.6g}"
            
        st.session_state.display_value = result_str
        st.rerun()
        
    except Exception as e:
        st.session_state.display_value = "Error"
        st.error(f"Error: {str(e)}")

# Display do Resultado
st.markdown(f"""
    <div style="
        border: 2px solid #5C4FFF;
        border-radius: 12px;
        background-color: #1A1C24;
        text-align: center;
        padding: 25px;
        margin-top: 15px;
    ">
        <span style="color: #8C82FF; font-size: 2.8rem; font-weight: 700; font-family: 'Inter', sans-serif;">
            {st.session_state.display_value}
        </span>
    </div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("""
    <div style="text-align: center; color: #6E707E; font-size: 0.75rem; margin-top: 25px; font-family: 'Inter', sans-serif;">
        🚀 Math Core 3000 • Python C++ Powered
    </div>
""", unsafe_allow_html=True)
