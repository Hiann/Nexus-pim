import streamlit as st
import time
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# Imports do Projeto
from styles import apply_theme, inject_sidebar_js
from utils import (get_produtos, criar_produto, deletar_produto, atualizar_produto, 
                   formatar_moeda, ProductValidator, converter_para_excel, gerar_sku_sugestao)
from components import render_kpi, render_card, render_charts

# --- LISTA MESTRA DE CATEGORIAS ---
CATEGORIAS = [
    "Eletrônicos", "Informática", "Móveis", "Gamer", "Moda", "Escritório", 
    "Casa & Cozinha", "Esportes & Lazer", "Ferramentas", "Automotivo", 
    "Brinquedos", "Beleza & Saúde", "Livros & Papelaria", "Outros"
]

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(
    page_title="Nexus PIM", 
    layout="wide", 
    page_icon="💠", 
    initial_sidebar_state="expanded" # MUDEI PARA EXPANDED PARA FORÇAR ELA A APARECER, O JS VAI FECHAR DEPOIS
)
apply_theme()
inject_sidebar_js()

# --- DIALOG (POP-UP) DE EDIÇÃO ---
@st.dialog("✏️ Editar Produto")
def abrir_modal_edicao(p):
    st.caption(f"Gerenciando SKU: {p['sku']}")
    
    with st.form(key=f"edit_form_{p['sku']}"):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome do Produto", value=p['nome'])
            try: cat_index = CATEGORIAS.index(p['categoria'])
            except ValueError: cat_index = 0 
            cat = st.selectbox("Categoria", CATEGORIAS, index=cat_index)
            
        with c2:
            val_preco = float(p['preco']) if p['preco'] else 0.0
            val_estoque = int(p['estoque']) if p['estoque'] else 0
            preco = st.number_input("Preço de Venda (R$)", value=val_preco, min_value=0.0, format="%.2f")
            estoque = st.number_input("Estoque Atual", value=val_estoque, min_value=0)
            
        img = st.text_input("URL da Imagem de Capa", value=p.get('url_imagem', ''))
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_cancel, col_save = st.columns([1, 1])
        with col_save:
            submit = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
        
        if submit:
            payload = {"sku": p['sku'], "nome": nome, "categoria": cat, "preco": preco, "estoque": estoque, "url_imagem": img}
            if atualizar_produto(p['sku'], payload):
                st.toast("Produto atualizado com sucesso!", icon="✅"); time.sleep(0.5); st.rerun()
            else:
                st.error("Erro ao atualizar. Verifique a conexão.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 10px; display: flex; align-items: center; gap: 14px; margin-bottom: 30px;">
            <div style="width: 42px; height: 42px; background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(59,130,246,0.4);">
                <span style="color: white; font-weight: 800; font-size: 20px;">N</span>
            </div>
            <div>
                <div style="font-weight: 700; font-size: 16px; color: #f4f4f5;">Nexus PIM</div>
                <div style="font-size: 11px; color: #a1a1aa;">ENTERPRISE V23.1</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(None, ["Dashboard", "Vitrine", "Novo Produto"], 
        icons=["bar-chart-fill", "grid-fill", "plus-square-fill"], default_index=0,
        styles={"container": {"padding": "0!important", "background": "transparent"}, "nav-link": {"font-size": "13px", "color": "#a1a1aa", "padding-left": "15px"}, "nav-link-selected": {"background": "#3b82f615", "color": "#3b82f6", "font-weight": "600", "border-left": "3px solid #3b82f6"}})

# --- ROTAS ---

# 1. DASHBOARD
if selected == "Dashboard":
    produtos = get_produtos()
    if not produtos:
        st.info("O sistema está pronto. Comece cadastrando produtos.")
    else:
        df = pd.DataFrame(produtos)
        df['preco'] = pd.to_numeric(df['preco'], errors='coerce').fillna(0)
        df['estoque'] = pd.to_numeric(df['estoque'], errors='coerce').fillna(0)
        
        c1, c2 = st.columns([4, 1.2])
        with c1: st.title("Visão Geral"); st.caption(f"Dados consolidados • {len(df)} produtos ativos")
        with c2:
            st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
            try: st.download_button("📥 Baixar Relatório", converter_para_excel(df), f"Report_{datetime.now().strftime('%Y%m%d')}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, type="primary")
            except: pass
        
        st.markdown("---")
        k1,k2,k3,k4 = st.columns(4)
        with k1: render_kpi("Produtos Totais", len(df), "📦", "#3b82f6")
        with k2: render_kpi("Valor Estoque", formatar_moeda((df['preco']*df['estoque']).sum()), "💰", "#10b981")
        with k3: render_kpi("Ticket Médio", formatar_moeda(df['preco'].mean()), "📈", "#f59e0b")
        with k4: render_kpi("Categorias", df['categoria'].nunique(), "🏷️", "#8b5cf6")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("""<div class="dashboard-card">""", unsafe_allow_html=True)
            render_charts(df)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # TABELA DE ESTOQUE COMPLETA
        st.markdown("##### 📊 Monitoramento de Estoque (Todos os Produtos)")
        if not df.empty:
            stock_df = df.sort_values('estoque')[['sku', 'nome', 'categoria', 'estoque']]
            st.dataframe(
                stock_df,
                column_config={
                    "sku": "Código",
                    "nome": "Produto",
                    "categoria": "Categoria",
                    "estoque": st.column_config.ProgressColumn(
                        "Nível de Estoque",
                        help="Visualização rápida do estoque",
                        format="%d un",
                        min_value=0,
                        max_value=int(df['estoque'].max()) if df['estoque'].max() > 0 else 100,
                    ),
                },
                hide_index=True,
                use_container_width=True,
                height=400
            )

# 2. VITRINE
elif selected == "Vitrine":
    produtos = get_produtos()
    if not produtos:
        st.warning("Nenhum produto cadastrado.")
    else:
        df = pd.DataFrame(produtos)
        df['preco'] = pd.to_numeric(df['preco'], errors='coerce').fillna(0)
        
        min_real = float(df['preco'].min())
        max_real = float(df['preco'].max())
        if min_real == max_real: max_real += 100.0

        with st.expander("🔎 Filtros & Busca", expanded=True):
            f1, f2, f3 = st.columns([2, 1.5, 1.5], gap="medium")
            with f1: query = st.text_input("Buscar", placeholder="Nome ou SKU...", label_visibility="collapsed")
            with f2: cat_sel = st.selectbox("Categoria", ["Todas"] + sorted(list(df['categoria'].unique())), label_visibility="collapsed")
            with f3: sort_sel = st.selectbox("Ordenar", ["Recentes", "Menor Preço", "Maior Preço", "A-Z"], label_visibility="collapsed")
            
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.caption("Filtrar por Faixa de Preço (R$)")
            
            p1, p2, p3 = st.columns([1, 1, 2], gap="medium")
            with p1: min_p = st.number_input("Mínimo", value=min_real, step=10.0, label_visibility="collapsed")
            with p2: max_p = st.number_input("Máximo", value=max_real, step=10.0, label_visibility="collapsed")

        # Lógica de Filtro
        df_show = df.copy()
        if query: df_show = df_show[df_show['nome'].str.contains(query, case=False) | df_show['sku'].str.contains(query, case=False)]
        if cat_sel != "Todas": df_show = df_show[df_show['categoria'] == cat_sel]
        df_show = df_show[(df_show['preco'] >= min_p) & (df_show['preco'] <= max_p)]
        
        if sort_sel == "Menor Preço": df_show = df_show.sort_values('preco')
        elif sort_sel == "Maior Preço": df_show = df_show.sort_values('preco', ascending=False)
        elif sort_sel == "A-Z": df_show = df_show.sort_values('nome')
        else: df_show = df_show.iloc[::-1]

        st.markdown(f"<div style='margin: 15px 0; color:#71717a; font-size:12px; font-weight:500;'>Encontrados: <b style='color:#f4f4f5'>{len(df_show)}</b> produtos</div>", unsafe_allow_html=True)

        if df_show.empty:
            st.info("Nenhum resultado encontrado para os filtros selecionados.")
        else:
            cols = st.columns(4)
            for idx, row in enumerate(df_show.to_dict('records')):
                with cols[idx % 4]:
                    render_card(row)
                    b1, b2 = st.columns(2)
                    with b1: 
                        if st.button("EDITAR", key=f"ed_{row['sku']}", use_container_width=True): abrir_modal_edicao(row)
                    with b2:
                        if st.button("EXCLUIR", key=f"del_{row['sku']}", type="primary", use_container_width=True):
                            deletar_produto(row['sku'])
                            st.rerun()

# 3. NOVO PRODUTO
elif selected == "Novo Produto":
    keys = ["f_sku", "f_nome", "f_price", "f_cost", "f_img"]
    for k in keys:
        if k not in st.session_state: st.session_state[k] = ""
    if "f_qty" not in st.session_state: st.session_state.f_qty = 10
    
    def cb_sku(): 
        if st.session_state.f_nome: st.session_state.f_sku = gerar_sku_sugestao(st.session_state.f_nome, st.session_state.f_cat)
        else: st.toast("Digite o nome primeiro.", icon="⚠️")
    
    def cb_save():
        sku = st.session_state.f_sku.upper().strip()
        ok_sku, msg_sku = ProductValidator.validate_sku(sku)
        val, ok_p, msg_p = ProductValidator.validate_price(st.session_state.f_price)
        
        if ok_sku and ok_p and st.session_state.f_nome:
            payload = {
                "sku": sku, "nome": st.session_state.f_nome, "categoria": st.session_state.f_cat, 
                "preco": val, "estoque": st.session_state.f_qty, "url_imagem": st.session_state.f_img
            }
            res = criar_produto(payload)
            if res and res.status_code in [200, 201]: 
                st.toast("Produto cadastrado com sucesso!", icon="🎉")
                for k in keys: st.session_state[k] = ""
                st.session_state.f_qty = 10
            elif res and res.status_code == 400: st.toast("Erro: SKU já existe.", icon="❌")
            else: st.toast("Erro no servidor.", icon="🔥")
        else: 
            st.toast(f"Dados inválidos: {msg_sku if not ok_sku else msg_p}", icon="⚠️")

    st.markdown("### ✨ Novo Cadastro"); st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.8, 1], gap="large")
    with c1:
        with st.container():
            st.markdown('<div class="nexus-card"><div class="section-header">📦 Dados Principais</div>', unsafe_allow_html=True)
            k1, k2 = st.columns([1, 2])
            with k1: st.text_input("SKU", key="f_sku", placeholder="Ex: NK-001"); st.button("⚡ Gerar Auto", on_click=cb_sku, use_container_width=True)
            with k2: st.text_input("Nome do Produto", key="f_nome", placeholder="Ex: Monitor Ultra")
            st.selectbox("Categoria", CATEGORIAS, key="f_cat")
            st.markdown('</div><br>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="nexus-card"><div class="section-header">💰 Precificação</div>', unsafe_allow_html=True)
            f1, f2, f3 = st.columns(3)
            with f1: st.text_input("Venda (R$)", key="f_price", placeholder="0,00")
            with f2: st.text_input("Custo (R$)", key="f_cost", placeholder="0,00")
            with f3: st.number_input("Estoque Inicial", key="f_qty", min_value=0)
            st.markdown('</div><br>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="nexus-card"><div class="section-header">🖼️ Mídia</div>', unsafe_allow_html=True)
            st.text_input("URL da Imagem", key="f_img", placeholder="https://..."); st.markdown('</div><br>', unsafe_allow_html=True)
        st.button("Cadastrar Produto", type="primary", use_container_width=True, on_click=cb_save)
    with c2:
        st.caption("PRÉ-VISUALIZAÇÃO")
        val, _, _ = ProductValidator.validate_price(st.session_state.f_price)
        render_card({
            "nome": st.session_state.f_nome or "Novo Produto", 
            "sku": st.session_state.f_sku or "---", 
            "categoria": st.session_state.f_cat, 
            "preco": val, 
            "estoque": st.session_state.f_qty, 
            "url_imagem": st.session_state.f_img
        })