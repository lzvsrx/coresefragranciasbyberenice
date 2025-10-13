import streamlit as st
import os
from datetime import datetime
from utils.database import (
    add_produto, get_all_produtos, update_produto, delete_produto, get_produto_by_id,
    export_produtos_to_csv, import_produtos_from_csv, generate_stock_pdf,
    mark_produto_as_sold
)
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")
# Lista de marcas de produtos ATUALIZADA.
MARCAS = [
    "Eudora", "O Boticário", "Jequiti", "Avon", "Mary Kay", "Natura",
    "Oui-Original-Unique-Individuel", "Pierre Alexander", "Tupperware" # NOVAS MARCAS ADICIONADAS
]

# Lista de estilos de produtos ATUALIZADA.
ESTILOS = [
    "Perfumaria", "Skincare", "Cabelo", "Corpo e Banho", "Make", "Masculinos", "Femininos Nina Secrets",
    "Marcas", "Infantil", "Casa", "Solar", "Maquiage", "Teen", "Kits e Presentes",
    "Cuidados com o Corpo", "Lançamentos",
    "Acessórios de Casa" # NOVO ESTILO ADICIONADO (Baseado em Tupperware e similares)
]

# Lista de tipos de produtos ATUALIZADA.
TIPOS = [
    "Perfumaria masculina", "Perfumaria feminina", "Body splash", "Body spray", "Eau de parfum",
    "Desodorantes", "Perfumaria infantil", "Perfumaria vegana", "Familia olfativa",
    "Clareador de manchas", "Anti-idade", "Protetor solar facial", "Rosto",
    "Tratamento para o rosto", "Acne", "Limpeza", "Esfoliante", "Tônico facial",
    "Kits de tratamento", "Tratamento para cabelos", "Shampoo", "Condicionador",
    "Leave-in e Creme para Pentear", "Finalizador", "Modelador", "Acessórios",
    "Kits e looks", "Boca", "Olhos", "Pincéis", "Paleta", "Unhas", "Sobrancelhas",
    "Kits de tratamento", "Hidratante", "Cuidados pós-banho", "Cuidados para o banho",
    "Barba", "Óleo corporal", "Cuidados íntimos", "Unissex", "Bronzeamento",
    "Protetor solar", "Depilação", "Mãos", "Lábios", "Pés", "Pós sol",
    "Protetor solar corporal", "Colônias", "Estojo", "Sabonetes",
    "Creme hidratante para as mãos", "Creme hidratante para os pés", "Miniseries",
    "Kits de perfumes", "Antissinais", "Máscara", "Creme bisnaga",
    "Roll On Fragranciado", "Roll On On Duty", "Sabonete líquido",
    "Sabonete em barra", "Shampoo 2 em 1", "Spray corporal", "Booster de Tratamento",
    "Creme para Pentear", "Óleo de Tratamento", "Pré-shampoo",
    "Sérum de Tratamento", "Shampoo e Condicionador",
    # NOVOS TIPOS DE PRODUTOS PARA CASA/TUPPERWARE ADICIONADOS:
    "Garrafas", "Armazenamentos", "Micro-ondas", "Servir", "Preparo",
    "Infantil", "Lazer/Outdoor", "Presentes"
]

st.set_page_config(page_title="Gerenciar Produtos - Cores e Fragrâncias")

def add_product_form():
    st.subheader("Adicionar Novo Produto")
    with st.form("add_product_form", clear_on_submit=True):
        nome = st.text_input("Nome do Produto", max_chars=150)
        col1, col2 = st.columns(2)
        with col1:
            preco = st.number_input("Preço (R$)", min_value=0.00, format="%.2f")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=0, step=1)
        marca = st.selectbox("Marca", MARCAS)
        estilo = st.selectbox("Estilo", ESTILOS)
        tipo = st.selectbox("Tipo de Produto", TIPOS)
        data_validade = st.date_input("Data de Validade")
        foto = st.file_uploader("Adicionar Foto do Produto", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("Adicionar Produto")

        if submitted:
            if not nome:
                st.error("Nome é obrigatório.")
                return
            photo_name = None
            if foto:
                photo_name = f"{int(datetime.now().timestamp())}_{foto.name}"
                if not os.path.exists("assets"):
                    os.makedirs("assets")
                with open(os.path.join("assets", photo_name), "wb") as f:
                    f.write(foto.getbuffer())
            add_produto(nome, float(preco), int(quantidade), marca, estilo, tipo, photo_name, data_validade.isoformat())
            st.success(f"Produto '{nome}' adicionado com sucesso!")
            st.rerun()

def manage_products_list():
    st.subheader("Lista de Produtos")
    produtos = get_all_produtos()
    if not produtos:
        st.info("Nenhum produto cadastrado.")
        return

    # Top action buttons: CSV export/import, PDF report
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button('Exportar CSV'):
            csv_path = os.path.join('data','produtos_export.csv')
            try:
                if not os.path.exists('data'):
                    os.makedirs('data')
                export_produtos_to_csv(csv_path)
                st.success('CSV exportado para ' + csv_path)
                st.download_button('Baixar CSV', data=open(csv_path,'rb').read(), file_name='produtos_export.csv')
            except Exception as e:
                st.error('Erro ao exportar CSV: ' + str(e))
    with col_b:
        uploaded_csv = st.file_uploader('Importar CSV', type=['csv'], key='import_csv')
        if uploaded_csv is not None:
            save_path = os.path.join('data','import_tmp.csv')
            if not os.path.exists('data'):
                os.makedirs('data')
            with open(save_path,'wb') as f:
                f.write(uploaded_csv.getbuffer())
            try:
                import_produtos_from_csv(save_path)
                st.success('Produtos importados com sucesso.')
                st.rerun()
            except Exception as e:
                st.error('Erro ao importar CSV: ' + str(e))
    with col_c:
        if st.button('Gerar Relatório PDF'):
            pdf_path = os.path.join('data','relatorio_estoque.pdf')
            try:
                if not os.path.exists('data'):
                    os.makedirs('data')
                generate_stock_pdf(pdf_path)
                st.success('PDF gerado: ' + pdf_path)
                with open(pdf_path,'rb') as f:
                    st.download_button('Baixar PDF', data=f.read(), file_name='relatorio_estoque.pdf')
            except Exception as e:
                st.error('Erro ao gerar PDF: ' + str(e))

    for p in produtos:
        produto_id = p.get("id")
        # Improved card-like layout
        with st.container(border=True): # Adicionado border para melhor visualização
            cols = st.columns([3,1,1])
            with cols[0]:
                st.markdown(f"### {p.get('nome')}  <small style='color:gray'>ID: {produto_id}</small>", unsafe_allow_html=True)
                st.write(f"**Preço:** R$ {float(p.get('preco')):.2f}   •   **Quantidade:** {p.get('quantidade')}")
                st.write(f"**Marca:** {p.get('marca')}   •   **Estilo:** {p.get('estilo')}   •   **Tipo:** {p.get('tipo')}")
                data_validade_str = p.get('data_validade')
                # Formata a data de validade para exibição (DD/MM/AAAA)
                if data_validade_str:
                    try:
                        validade_formatada = datetime.fromisoformat(data_validade_str).strftime('%d/%m/%Y')
                    except ValueError:
                        validade_formatada = data_validade_str # Se a formatação falhar, mostra o original
                else:
                    validade_formatada = '-'
                    
                st.write(f"**Validade:** {validade_formatada}")
                
                # Botão de venda adicionado aqui
                if p.get("quantidade") > 0:
                    if st.button("Vender", key=f'sell_{produto_id}'):
                        mark_produto_as_sold(produto_id, 1) # Vende 1 unidade
                        st.success(f"1 unidade de '{p.get('nome')}' foi vendida.")
                        st.rerun()
                else:
                    st.info("Fora de estoque.")

            with cols[1]:
                if p.get('foto') and os.path.exists(os.path.join('assets', p.get('foto'))):
                    st.image(os.path.join('assets', p.get('foto')), width=120)
                else:
                    st.info('Sem foto')
            with cols[2]:
                role = st.session_state.get('role','staff')
                # Only admins can delete products; staff can add/edit
                if st.button('Editar', key=f'mod_{produto_id}'):
                    st.session_state['edit_product_id'] = produto_id
                    st.session_state['edit_mode'] = True
                    st.rerun()
                if role == 'admin':
                    if st.button('Remover', key=f'rem_{produto_id}'):
                        delete_produto(produto_id)
                        st.warning(f"Produto '{p.get('nome')}' removido.")
                        st.rerun()
                else:
                    st.text('Remover (admin)')
            
            st.markdown("---") # Separador para o próximo produto

    if st.session_state.get('edit_mode'):
        show_edit_form()

def show_edit_form():
    produto_id = st.session_state.get('edit_product_id')
    produto = get_produto_by_id(produto_id)
    if not produto:
        st.error("Produto não encontrado.")
        st.session_state["edit_mode"] = False
        return

    st.subheader(f"Editar Produto: {produto.get('nome')}")
    # Converte a data de validade para o formato que o st.date_input espera
    default_date = None
    if produto.get("data_validade"):
        try:
            default_date = datetime.fromisoformat(produto.get("data_validade")).date()
        except ValueError:
            default_date = None

    with st.form("edit_product_form"):
        nome = st.text_input("Nome", value=produto.get("nome"))
        col1, col2 = st.columns(2)
        with col1:
            preco = st.number_input("Preço (R$)", value=float(produto.get("preco")), format="%.2f")
        with col2:
            quantidade = st.number_input("Quantidade", value=int(produto.get("quantidade")), step=1)
        marca = st.selectbox("Marca", MARCAS, index=MARCAS.index(produto.get("marca")) if produto.get("marca") in MARCAS else 0)
        estilo = st.selectbox("Estilo", ESTILOS, index=ESTILOS.index(produto.get("estilo")) if produto.get("estilo") in ESTILOS else 0)
        tipo = st.selectbox("Tipo", TIPOS, index=TIPOS.index(produto.get("tipo")) if produto.get("tipo") in TIPOS else 0)
        data_validade = st.date_input("Data de Validade", value=default_date)
        uploaded = st.file_uploader("Alterar Foto", type=["jpg","png","jpeg"])
        save = st.form_submit_button("Salvar Alterações")
        cancel = st.form_submit_button("Cancelar Edição")


        if save:
            photo_name = produto.get("foto")
            if uploaded:
                photo_name = f"{int(datetime.now().timestamp())}_{uploaded.name}"
                if not os.path.exists("assets"):
                    os.makedirs("assets")
                with open(os.path.join("assets", photo_name), "wb") as f:
                    f.write(uploaded.getbuffer())
            
            # Validação: nome não pode ser vazio
            if not nome:
                st.error("Nome é obrigatório.")
                return

            # Garantir que a data de validade seja salva em formato ISO ou nulo.
            validade_iso = data_validade.isoformat() if data_validade else None

            update_produto(produto_id, nome, float(preco), int(quantidade), marca, estilo, tipo, photo_name, validade_iso)
            st.success("Produto atualizado com sucesso!")
            st.session_state["edit_mode"] = False
            st.rerun()
        
        if cancel:
            st.session_state["edit_mode"] = False
            st.rerun()


# Página principal de gerenciamento (somente se logado)
if not st.session_state.get("logged_in"):
    st.error("Acesso negado. Faça login na área administrativa para gerenciar produtos.")
    st.info("Vá para a página 'Área Administrativa' para entrar ou criar um admin.")
else:
    st.sidebar.markdown(f"**Olá, {st.session_state.get('username')} ({st.session_state.get('role','staff')})**")
    action = st.sidebar.selectbox("Ação", ["Adicionar Produto", "Visualizar / Modificar / Remover Produtos"])
    if action == "Adicionar Produto":
        add_product_form()
    else:
        manage_products_list()