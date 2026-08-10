@st.cache_resource
def get_calculator():
    """Compila e carrega o módulo C++"""
    try:
        import calc_backend
        return calc_backend.AdvancedCalculator(), "C++"
    except ImportError:
        with st.spinner("🔧 Compilando C++ backend... (pode levar 2-3 minutos)"):
            try:
                # Instalar dependências do sistema
                import subprocess
                
                # Atualizar e instalar compilador
                subprocess.run(
                    "apt-get update && apt-get install -y build-essential g++ python3-dev",
                    shell=True, check=True, capture_output=True
                )
                
                # Instalar pybind11 via pip
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "pybind11"],
                    check=True, capture_output=True
                )
                
                # Compilar o módulo
                result = subprocess.run(
                    [sys.executable, "setup.py", "build_ext", "--inplace"],
                    check=True, capture_output=True, text=True
                )
                
                # Tentar importar novamente
                import calc_backend
                return calc_backend.AdvancedCalculator(), "C++"
                
            except Exception as e:
                st.warning(f"⚠️ C++ compilation failed, using Python backend")
                return PythonCalculator(), "Python"
