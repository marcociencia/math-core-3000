@st.cache_resource
def get_calculator():
    """Compila C++ usando packages.txt do Streamlit"""
    try:
        import calc_backend
        return calc_backend.AdvancedCalculator(), "C++"
    except ImportError:
        with st.spinner("🔧 Compilando C++..."):
            import subprocess
            
            # O Streamlit Cloud já instalou build-essential via packages.txt
            # Basta instalar pybind11 e compilar
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pybind11"],
                check=True, capture_output=True
            )
            
            # Compila diretamente
            subprocess.run(
                [sys.executable, "setup.py", "build_ext", "--inplace"],
                check=True, capture_output=True
            )
            
            import calc_backend
            return calc_backend.AdvancedCalculator(), "C++"
