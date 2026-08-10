import streamlit as st
import streamlit.components.v1 as components
import subprocess
import sys
import os

# Tentar importar, se falhar, compilar automaticamente
try:
    import calc_backend
except ImportError:
    st.warning("Compiling C++ module... This may take a minute.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    import calc_backend

# Resto do seu código permanece igual...
