import streamlit as st
from utils.database import get_all_produtos
import os
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")

st.set_page_config(page_title="Estoque - Cores e Fragrâncias")

st.title("📦 Estoque Completo")

produtos = get_all_produtos()

if not produtos:
    st.info("Nenhum produto cadastrado no estoque.")
else:
    marcas = sorted(list({p.get("marca") for p in produtos if p.get("marca")}))
    estilos = sorted(list({p.get("estilo") for p in produtos if p.get("estilo")}))
    tipos = sorted(list({p.get("tipo") for p in produtos if p.get("tipo")}))

    col1, col2, col3 = st.columns(3)
    with col1:
        marca_filtro = st.selectbox("Filtrar por Marca", ["Todas"] + marcas)
    with col2:
        estilo_filtro = st.selectbox("Filtrar por Estilo", ["Todos"] + estilos)
    with col3:
        tipo_filtro = st.selectbox("Filtrar por Tipo", ["Todos"] + tipos)

    produtos_filtrados = produtos
    if marca_filtro != "Todas":
        produtos_filtrados = [p for p in produtos_filtrados if p.get("marca") == marca_filtro]
    if estilo_filtro != "Todos": 
        produtos_filtrados = [p for p in produtos_filtrados if p.get("estilo") == estilo_filtro]
    if tipo_filtro != "Todos":
        produtos_filtrados = [p for p in produtos_filtrados if p.get("tipo") == tipo_filtro]

    st.markdown("---")
    st.subheader(f"{len(produtos_filtrados)} produtos encontrados")

    for p in produtos_filtrados:
        st.markdown(f"### **{p.get('nome')}**")
        st.write(f"**Preço:** R$ {float(p.get('preco')):.2f}")
        st.write(f"**Quantidade:** {p.get('quantidade')}")
        st.write(f"**Marca:** {p.get('marca')}")
        st.write(f"**Estilo:** {p.get('estilo')}")
        st.write(f"**Tipo:** {p.get('tipo')}")
        st.write(f"**Validade:** {p.get('data_validade')}")
        if p.get("foto"):
            try:
                st.image(f"assets/{p.get('foto')}", width=180)
            except Exception:
                st.info("Erro ao carregar imagem; verifique assets/")
        st.markdown("---")
