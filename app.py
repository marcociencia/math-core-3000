import streamlit as st
import streamlit.components.v1 as components
import calc_backend

# 1. Configuração da Página
st.set_page_config(page_title="Super Calculator", page_icon="⚡", layout="centered")

# 2. Injeção de CSS (Customização Visual)
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .custom-title {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        letter-spacing: 1px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        width: 100%;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
        color: white;
    }
    .result-box {
        background-color: #28a745;
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='custom-title'>⚡ Advanced Web Calculator</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. Inicialização do Motor C++
calc = calc_backend.AdvancedCalculator()

# 4. Interface de Usuário
col1, col2 = st.columns(2)
num1 = col1.number_input("Enter First Number", value=0.0)
num2 = col2.number_input("Enter Second Number", value=0.0)

operation = st.selectbox("Choose Operation", ["Add", "Subtract", "Multiply", "Divide", "Power"])

# 5. Lógica e Injeção de JavaScript
if st.button("Calculate"):
    try:
        # Chamadas para o C++
        if operation == "Add": result = calc.add(num1, num2)
        elif operation == "Subtract": result = calc.subtract(num1, num2)
        elif operation == "Multiply": result = calc.multiply(num1, num2)
        elif operation == "Divide": result = calc.divide(num1, num2)
        elif operation == "Power": result = calc.power(num1, num2)
        
        # Renderiza o resultado com o CSS customizado
        st.markdown(f"<div class='result-box'>Result: {result}</div>", unsafe_allow_html=True)
        
        # Executa código JavaScript no navegador do usuário
        js_code = """
        <script>
            console.log("Calculation successful! Value: """ + str(result) + """");
            alert("Calculation Completed Successfully!");
        </script>
        """
        components.html(js_code, height=0)

    except Exception as e:
        st.error(f"Error: {str(e)}")
