import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import formatar_moeda

def render_kpi(title, value, icon, color="#3b82f6"):
    # HTML do Card de KPI
    html = f"""
<div style="background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 20px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom: 12px;">
        <span style="color: #a1a1aa; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{title}</span>
        <div style="color: {color}; background: {color}15; width: 28px; height: 28px; border-radius: 8px; display:flex; align-items:center; justify-content:center; font-size: 14px;">{icon}</div>
    </div>
    <div style="font-size: 24px; font-weight: 700; color: #f4f4f5; letter-spacing: -0.5px;">{value}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

def render_card(p):
    img = p.get("url_imagem")
    if not img or len(img) < 5: 
        img = "https://placehold.co/600x400/18181b/27272a?text=Sem+Imagem"
    
    price = formatar_moeda(p['preco'])
    stock = p['estoque']
    
    # Badges de Status
    if stock == 0: 
        badge = '<span style="color:#f87171; background:#450a0a; border:1px solid #7f1d1d; padding:3px 8px; border-radius:4px; font-size:10px; font-weight:600;">ESGOTADO</span>'
    elif stock < 5: 
        badge = f'<span style="color:#fbbf24; background:#451a03; border:1px solid #78350f; padding:3px 8px; border-radius:4px; font-size:10px; font-weight:600;">RESTAM {stock}</span>'
    else: 
        badge = '<span style="color:#34d399; background:#064e3b; border:1px solid #065f46; padding:3px 8px; border-radius:4px; font-size:10px; font-weight:600;">DISPONÍVEL</span>'
    
    # HTML do Card
    html = f"""
<div class="nexus-card" style="display: flex; flex-direction: column; height: 100%; overflow: hidden; border-radius: 12px; background: #18181b;">
    <div style="height: 180px; background: #0c0c0e; display: flex; align-items: center; justify-content: center; padding: 20px; border-bottom: 1px solid #27272a; position: relative;">
        <img src="{img}" style="max-height: 100%; max-width: 100%; object-fit: contain; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));">
        <div style="position: absolute; top: 10px; right: 10px;">{badge}</div>
    </div>
    <div style="padding: 16px; flex-grow: 1; display: flex; flex-direction: column;">
        <div style="font-size: 10px; font-weight: 700; color: #60a5fa; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px;">{p['categoria']}</div>
        <div style="font-size: 14px; font-weight: 600; color: #f4f4f5; margin-bottom: 6px; line-height: 1.4; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{p['nome']}</div>
        <div style="font-size: 11px; color: #52525b; font-family: monospace; margin-bottom: 16px;">SKU: {p['sku']}</div>
        <div style="margin-top: auto; padding-top: 12px; border-top: 1px solid #27272a; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <div style="font-size: 10px; color: #a1a1aa; margin-bottom: 2px;">Valor Unitário</div>
                <div style="font-size: 18px; font-weight: 700; color: #f4f4f5;">{price}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 10px; color: #a1a1aa; margin-bottom: 2px;">Estoque</div>
                <div style="font-size: 13px; font-weight: 600; color: #e4e4e7;">{stock} un</div>
            </div>
        </div>
    </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

def render_charts(df):
    if df.empty: return
    c1, c2 = st.columns([2, 1], gap="medium")
    
    # Configuração Global do Plotly (Tema Escuro)
    layout_theme = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#a1a1aa"),
        hoverlabel=dict(
            bgcolor="#18181b", 
            bordercolor="#27272a", 
            font_size=12, 
            font_family="Inter",
            font_color="#ffffff"
        )
    )
    
    with c1:
        st.markdown("##### 📊 Receita Estimada (Todos os Produtos)")
        df['total'] = df['preco'] * df['estoque']
        
        # 1. MOSTRAR TODOS (Removemos o .head() ou .nlargest())
        # Ordenamos pelo total para que o gráfico de barras fique organizado do maior para o menor
        all_data = df.sort_values('total', ascending=True)
        
        # 2. ALTURA DINÂMICA (Cresce conforme a quantidade de produtos)
        # Mínimo de 350px, adiciona 35px por produto extra
        chart_height = max(350, len(all_data) * 35 + 50)

        fig = go.Figure(go.Bar(
            x=all_data['total'], 
            y=all_data['nome'], 
            orientation='h',
            marker=dict(color='#3b82f6', cornerradius=4),
            texttemplate='  R$ %{x:,.0f}', 
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Receita Total: R$ %{x:,.2f}<extra></extra>'
        ))
        
        # Ajuste do eixo X para dar espaço aos textos de valor (multiplicamos max por 1.3)
        max_val = all_data['total'].max() if not all_data.empty else 100
        
        fig.update_layout(
            **layout_theme,
            margin=dict(l=0,r=50,t=20,b=0), 
            height=chart_height, # Aplica a altura calculada
            xaxis=dict(showgrid=False, showticklabels=False, range=[0, max_val * 1.3]),
            yaxis=dict(showgrid=False, tickfont=dict(size=12))
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("##### 📦 Mix de Categorias")
        fig2 = go.Figure(go.Pie(
            labels=df['categoria'], 
            values=df['estoque'], 
            hole=0.65,
            marker=dict(colors=px.colors.qualitative.Pastel),
            textinfo='none',
            hovertemplate='<b>%{label}</b><br>Qtd: %{value}<br>Pct: %{percent}<extra></extra>'
        ))
        
        fig2.update_layout(
            **layout_theme,
            margin=dict(l=0,r=0,t=20,b=0), 
            height=350, # Altura fixa para o donut
            showlegend=False,
            annotations=[dict(text=str(len(df)), x=0.5, y=0.5, font_size=32, showarrow=False, font_color="white", font_weight="bold")]
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})