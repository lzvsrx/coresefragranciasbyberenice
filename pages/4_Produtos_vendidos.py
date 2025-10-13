import streamlit as st
from utils.database import get_all_produtos
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")

st.set_page_config(page_title="Produtos Vendidos - Cores e Fragrâncias")

st.title("💰 Produtos Vendidos")

produtos_vendidos = [p for p in get_all_produtos() if p.get("vendido") == 1]

if not produtos_vendidos:
    st.info("Nenhum produto foi vendido ainda.")
else:
    for p in produtos_vendidos:
        st.markdown(f"### **{p.get('nome')}**")
        st.write(f"**Preço de Venda:** R$ {float(p.get('preco')):.2f}")
        st.write(f"**Data da Venda:** {p.get('data_ultima_venda') or 'N/A'}")
        st.write(f"**Marca:** {p.get('marca')}")
        st.markdown("---")