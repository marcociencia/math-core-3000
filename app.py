import streamlit as st
import streamlit.components.v1 as components
import sys
import os

# Tentar importar o módulo compilado
try:
    import calc_backend
except ImportError:
    st.error("Compilando o módulo C++ pela primeira vez...")
    # Compilar o módulo
    os.system("pip install -e .")
    import calc_backend

# Resto do código permanece igual...
