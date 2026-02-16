import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
            /* IMPORTANDO FONTE PROFISSIONAL (INTER) */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            :root {
                --bg-main: #09090b;      /* Fundo Preto Profundo */
                --bg-card: #18181b;      /* Cinza Chumbo */
                --border: #27272a;       /* Borda Sutil */
                --text-main: #f4f4f5;    /* Branco Gelo */
                --text-sub: #a1a1aa;     /* Cinza Texto */
                --accent: #3b82f6;       /* Azul Enterprise */
                --accent-hover: #2563eb; /* Azul Mais Escuro */
            }

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
            }

            /* --- CORREÇÃO DO CABEÇALHO --- */
            /* Não escondemos mais o header, apenas deixamos transparente */
            [data-testid="stHeader"] {
                background-color: rgba(0,0,0,0);
            }
            
            /* Esconde apenas o botão de deploy e footer, mantendo o menu acessível */
            .stDeployButton {display: none;}
            footer {visibility: hidden;}
            
            /* LARGURA E ESPAÇAMENTO */
            .block-container {
                padding-top: 2rem; 
                padding-bottom: 2rem;
                max-width: 1600px;
            }

            /* --- SIDEBAR REFINADA --- */
            [data-testid="stSidebar"] {
                background-color: #050505; /* Quase preto */
                border-right: 1px solid var(--border);
            }

            /* Ajuste para o conteúdo não ficar colado no topo */
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1rem;
            }
            
            /* SCROLLBAR PERSONALIZADA */
            section[data-testid="stSidebar"] ::-webkit-scrollbar {
                width: 4px;
                height: 4px;
            }
            section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
                background: #050505; 
            }
            section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
                background: #27272a; 
                border-radius: 4px;
            }
            section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb:hover {
                background: #3f3f46; 
            }

            /* INPUTS MODERNOS */
            .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
                background-color: #121214 !important;
                border: 1px solid #27272a !important;
                color: #e4e4e7 !important;
                border-radius: 6px !important;
                height: 42px;
                transition: border 0.2s;
            }
            .stTextInput input:focus, .stNumberInput input:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 1px var(--accent) !important;
            }

            /* BOTÕES */
            button[kind="primary"] {
                background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%) !important;
                border: none !important;
                box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
                transition: transform 0.1s !important;
            }
            button[kind="primary"]:active {
                transform: scale(0.98) !important;
            }

            /* CARDS */
            .nexus-card {
                transition: all 0.3s ease;
                border: 1px solid var(--border);
            }
            .nexus-card:hover {
                transform: translateY(-4px);
                border-color: var(--accent);
                box-shadow: 0 10px 30px -10px rgba(59, 130, 246, 0.25);
            }
            
            /* DASHBOARD CONTAINERS */
            .dashboard-card {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .js-plotly-plot .plotly .modebar {display: none !important;}
            
            /* TABELA */
            [data-testid="stDataFrame"] {
                border: 1px solid #27272a;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def inject_sidebar_js():
    st.markdown("""
        <script>
            // Tenta fechar a sidebar ao iniciar, mas sem impedir que o usuário abra
            const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                 // Lógica opcional: se quiser forçar o fechamento via JS
            }
        </script>
    """, unsafe_allow_html=True)