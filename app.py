import streamlit as st
from utils.database import create_tables


# Inicializa o banco de dados e as tabelas
create_tables()
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")

st.set_page_config(
    page_title="Cores e Fragrâncias by Berenice",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌸 Cores e Fragrâncias by Berenice 🌸")

st.markdown("""
Este é o aplicativo para **gerenciamento de estoque** da loja.

Use o menu lateral (ícone das páginas do Streamlit) para navegar entre:
- 📦 Estoque Completo
- 💰 Produtos Vendidos
- 🔐 Área Administrativa (login / cadastro)
- 🛠️ Gerenciar Produtos (somente após login)
""")

# Mostra logo (verifique assets/logo.png)
try:
    st.image("assets/logo.png", width=250)
except Exception:
    st.info("Coloque a sua logo em assets/logo.png para exibir aqui.")

# Botão de Logout (mostrado no sidebar se estiver logado)
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    if st.sidebar.button("Sair"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()