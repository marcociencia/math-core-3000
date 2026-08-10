# ============================================
# COMPILAÇÃO AUTOMÁTICA DO C++ (VERSÃO CORRIGIDA)
# ============================================
@st.cache_resource
def get_calculator():
    """Compila e carrega o módulo C++ automaticamente"""
    try:
        # Tenta importar primeiro (se já foi compilado)
        import calc_backend
        st.success("✅ C++ Backend Loaded!")
        return calc_backend.AdvancedCalculator(), "C++"
    except ImportError:
        # Se falhar, instala compilador e compila
        with st.spinner("🔧 Instalando compilador C++ e compilando módulo... (2-3 minutos)"):
            try:
                # Passo 1: Instalar compilador C++
                st.info("📦 Instalando g++ compiler...")
                os.system("sudo apt-get update -qq")
                os.system("sudo apt-get install -y -qq build-essential g++ python3-dev")
                
                # Passo 2: Instalar pybind11
                st.info("📦 Instalando pybind11...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pybind11>=2.10.0"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Passo 3: Compilar o módulo C++
                st.info("🔨 Compilando calc_backend...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-e", "."],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Passo 4: Verificar se compilou
                import calc_backend
                st.success("✅ C++ Backend compilado com sucesso!")
                return calc_backend.AdvancedCalculator(), "C++"
                
            except Exception as e:
                st.warning(f"⚠️ Não foi possível compilar C++: {str(e)[:100]}...")
                st.info("Usando Python como fallback...")
                return PythonCalculator(), "Python (fallback)"
