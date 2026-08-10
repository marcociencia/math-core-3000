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

# Custom CSS for elegant design
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
        font-family: 'JetBrains Mono', monospace;
    }
    
    .calculator-container {
        background: rgba(38, 39, 48, 0.8);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.2);
        backdrop-filter: blur(10px);
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
    
    .result-label {
        color: #8B8B8B;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
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
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(108, 99, 255, 0.4);
    }
    
    .stSelectbox > div > div {
        background: rgba(38, 39, 48, 0.8);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 10px;
    }
    
    .stNumberInput > div > div {
        background: rgba(38, 39, 48, 0.8);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 10px;
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
</style>
""", unsafe_allow_html=True)

# Try to import C++ backend, compile if needed
@st.cache_resource
def get_calculator():
    try:
        import calc_backend
        return calc_backend.AdvancedCalculator()
    except ImportError:
        with st.spinner("🔧 Compiling C++ backend for maximum performance..."):
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-e", "."],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                import calc_backend
                return calc_backend.AdvancedCalculator()
            except:
                st.error("Failed to compile C++ backend. Using Python fallback.")
                return None

# Fallback Python calculator
class PythonCalculator:
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
    def percentage(self, a, b): return (a * b) / 100
    def factorial(self, n):
        if n < 0: raise ValueError("Factorial of negative number!")
        if n > 20: raise ValueError("Number too large!")
        result = 1
        for i in range(2, int(n) + 1): result *= i
        return result

# Initialize calculator
calc = get_calculator()
if calc is None:
    calc = PythonCalculator()
    using_cpp = False
else:
    using_cpp = True

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Main Interface
st.markdown('<h1 class="main-title">⚡ Math Core 3000</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ultra-Fast Calculation Engine</p>', unsafe_allow_html=True)

# Calculator Container
with st.container():
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
    # Operation selector with icons
    operations = {
        "➕ Addition": "add",
        "➖ Subtraction": "subtract",
        "✖️ Multiplication": "multiply",
        "➗ Division": "divide",
        "🔢 Power": "power",
        "√ Square Root": "sqrt",
        "💯 Percentage": "percentage",
        "❗ Factorial": "factorial"
    }
    
    selected_op = st.selectbox(
        "Select Operation",
        list(operations.keys()),
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        num1 = st.number_input(
            "First Number",
            value=0.0,
            format="%.4f",
            help="Enter the first number"
        )
    
    with col2:
        if operations[selected_op] in ["sqrt", "factorial"]:
            num2 = 0  # Not used
            st.number_input(
                "Second Number",
                value=0.0,
                disabled=True,
                help="Not required for this operation"
            )
        else:
            num2 = st.number_input(
                "Second Number",
                value=0.0,
                format="%.4f",
                help="Enter the second number"
            )
    
    # Calculate button
    if st.button("🚀 Calculate", use_container_width=True):
        try:
            operation_func = getattr(calc, operations[selected_op])
            
            if operations[selected_op] in ["sqrt", "factorial"]:
                result = operation_func(num1)
                expression = f"{operations[selected_op].split()[-1].lower()}({num1})"
            else:
                result = operation_func(num1, num2)
                expression = f"{num1} {operations[selected_op].split()[1]} {num2}"
            
            # Display result
            st.markdown(f"""
                <div class="result-display">
                    <div class="result-label">Result</div>
                    <div class="result-number">{result:.6g}</div>
                    <div style="color: #8B8B8B; font-size: 0.8rem; margin-top: 0.5rem;">
                        {expression} = {result:.6g}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add to history
            st.session_state.history.append({
                'expression': expression,
                'result': result,
                'timestamp': time.strftime("%H:%M:%S")
            })
            
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# History section
if st.session_state.history:
    with st.expander("📜 Calculation History", expanded=False):
        for item in reversed(st.session_state.history[-5:]):  # Show last 5
            st.markdown(f"""
                <div class="history-item">
                    <strong>{item['expression']}</strong> = {item['result']:.6g}
                    <span style="color: #8B8B8B; float: right;">{item['timestamp']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

# Footer
st.markdown(f"""
    <div class="footer">
        🚀 Powered by {'C++' if using_cpp else 'Python'} Backend | 
        Math Core 3000 v1.0.0 | 
        Made with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### 🧮 About")
    st.markdown(f"""
    **Backend:** {'⚡ C++ (Ultra Fast)' if using_cpp else '🐍 Python (Standard)'}
    
    **Features:**
    - Basic arithmetic
    - Advanced operations
    - Calculation history
    - Beautiful UI
    
    **Tech Stack:**
    - Frontend: Streamlit
    - Backend: C++/Python
    - Binding: PyBind11
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Operations", len(st.session_state.history))
