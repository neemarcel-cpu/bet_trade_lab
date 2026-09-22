import streamlit as st
import pandas as pd
import requests
import datetime
import os
import plotly.graph_objects as go

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & CSS DARK FINTECH COM ELEMENTOS DE ALTO CONTRASTE
# =========================================================================
st.set_page_config(
    page_title="AlphaBet | Terminal Quantitativo & Backoffice",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Inversão da barra lateral para o lado DIREITO da tela */
    section[data-testid="stSidebar"] {
        order: 2 !important;
        border-left: 1px solid #232b3e !important;
        border-right: none !important;
        background-color: #10141d !important;
    }
    div[data-testid="stSidebarCollapseButton"] {
        order: 2 !important;
    }
    .main .block-container {
        order: 1 !important;
    }
    div.stApp > header {
        display: block;
    }
    div.stApp > div:first-child {
        flex-direction: row-reverse !important;
    }

    /* Fundo da Aplicação */
    .stApp {
        background-color: #0b0e14;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Legendas e Títulos dos Campos em Branco Nítido */
    label[data-testid="stWidgetLabel"] p,
    .stSelectbox label p,
    .stNumberInput label p,
    .stSlider label p,
    .stTextInput label p {
        color: #f8fafc !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px;
    }

    /* FORMULÁRIO VIP: CAIXAS BRANCAS COM TEXTO ESCURO */
    div[data-testid="stForm"] div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stForm"] input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stForm"] input::placeholder {
        color: #64748b !important;
        font-weight: 400 !important;
    }

    /* BOTÃO DO FORMULÁRIO VIP */
    div[data-testid="stForm"] div.stButton > button {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #f59e0b !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35) !important;
        width: 100% !important;
    }
    div[data-testid="stForm"] div.stButton > button p {
        color: #0f172a !important;
        font-weight: 800 !important;
    }

    /* BOTÕES DA BARRA LATERAL */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        width: 100% !important;
        font-weight: 600 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        margin-bottom: 6px !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] div.stButton > button p {
        color: inherit !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Selectboxes Gerais */
    div[data-baseweb="select"] > div {
        background-color: #141923 !important;
        border: 1px solid #232b3e !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }

    /* Botão Principal do Backtest */
    .main div.stButton > button {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: 1px solid #3b82f6 !important;
        padding: 10px 24px !important;
    }
    .main div.stButton > button p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Cards e Badges */
    .metric-card {
        background: #141923;
        border: 1px solid #232b3e;
        border-radius: 10px;
        padding: 16px;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-positive { color: #10b981 !important; }
    .metric-negative { color: #ef4444 !important; }
    .metric-accent { color: #38bdf8 !important; }

    .match-card {
        background: #141923;
        border: 1px solid #232b3e;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .live-badge {
        background: #ef4444;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .vip-badge {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #000;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 800;
    }
    .admin-badge {
        background: #6366f1;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 800;
    }

    .vip-gate-box {
        background: linear-gradient(180deg, #141923 0%, #0d121c 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #232b3e; padding-bottom: 14px; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; display: flex; align-items: center; gap: 10px;">
            <span>⚡ ALPHABET</span> 
            <span style="font-size: 0.8rem; background: #1e293b; color: #38bdf8; padding: 4px 10px; border-radius: 20px; border: 1px solid #38bdf8;">TERMINAL QUANT</span>
        </h1>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.9rem;">Backtest, Scanner In-Play, Inteligência VIP e Backoffice de Leads</p>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.8rem; color: #10b981; font-weight: 600;">● SISTEMA CONECTADO</span><br>
        <span style="font-size: 0.75rem; color: #64748b;">Feeds: Football-Data & API-Sports</span>
    </div>
</div>
""", unsafe_allow_html=True)

api_key = st.secrets.get("API_FOOTBALL_KEY", "")
admin_password = st.secrets.get("ADMIN_PASSWORD", "admin123")  # Senha padrão caso não cadastrada nos secrets

if "lead_desbloqueado" not in st.session_state:
    st.session_state.lead_desbloqueado = False

if "modulo_atual" not in st.session_state:
    st.session_state.modulo_atual = "🔴 Radar In-Play (Ao Vivo)"

# =========================================================================
# BARRA LATERAL À DIREITA COM MENU COMPLETO
# =========================================================================
with st.sidebar:
    st.markdown("<h3 style='font-size:1.15rem; color:#f8fafc; border-bottom: 1px solid #232b3e; padding-bottom: 8px;'>📌 Módulos</h3>", unsafe_allow_html=True)
    
    if st.button("🔴 Radar In-Play (Ao Vivo)"):
        st.session_state.modulo_atual = "🔴 Radar In-Play (Ao Vivo)"

    if st.button("👑 Análises VIP (Pré-Jogo)"):
        st.session_state.modulo_atual = "👑 Análises VIP (Pré-Jogo)"
    
    if st.button("🧪 Backtest Histórico (Área VIP)"):
        st.session_state.modulo_atual = "🧪 Backtest Histórico (Área VIP)"

    if st.button("📅 Agenda (Próximos Jogos)"):
        st.session_state.modulo_atual = "📅 Agenda (Próximos Jogos)"

    if st.button("🧮 Calculadora de Valor (+EV)"):
        st.session_state.modulo_atual = "🧮 Calculadora de Valor (+EV)"

    st.markdown("<br><div style='border-top: 1px solid #232b3e; padding-top: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🔒 Painel Admin (Leads)"):
        st.session_state.modulo_atual = "🔒 Painel Admin (Leads)"

    st.markdown("---")
    st.markdown("<div style='color:#94a3b8; font-size:0.8rem;'>Área ativa no momento:</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#38bdf8; font-weight:700; font-size:0.95rem;'>{st.session_state.modulo_atual}</div>", unsafe_allow_html=True)

# Função Auxiliar: Barreira de Entrada para Visitantes na Área VIP
def renderizar_barreira_lead(titulo_area):
    st.markdown(f"""
    <div class="vip-gate-box">
        <span class="vip-badge">ÁREA EXCLUSIVA DE ASSINANTES</span>
        <h2 style="margin: 12px 0 6px 0; color: #f8fafc; font-size: 1.5rem;">{titulo_area}</h2>
        <p style="color: #94a3b8; max-width: 650px; margin: 0 auto 16px auto; font-size: 0.95rem;">
            Desbloqueie acesso imediato ao <b>Simulador de 5 Anos de Backtest</b>, modelos de <b>xG</b>, 
            e projeções quantitativas preenchendo seus dados abaixo:
        </p>
        <p style="color: #f59e0b; font-weight: 700; font-size: 0.92rem;">
            🔓 Acesso 100% gratuito por tempo limitado:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_center, _ = st.columns([2, 1])
    with col_center:
        with st.form("form_captura_lead"):
            st.markdown("<h4 style='font-size:1.1rem; color:#f8fafc; margin-bottom:12px;'>Ficha de Cadastro VIP</h4>", unsafe_allow_html=True)
            nome_cliente = st.text_input("Nome Completo", placeholder="Digite seu nome completo...")
            email_cliente = st.text_input("E-mail Principal", placeholder="seuemail@provedor.com")
            whatsapp_cliente = st.text_input("WhatsApp com DDD", placeholder="(11) 99999-8888")
            
            enviar_lead = st.form_submit_button("🚀 Liberar Acesso VIP Agora")

            if enviar_lead:
                if nome_cliente.strip() and "@" in email_cliente and whatsapp_cliente.strip():
                    arquivo_leads = "leads_capturados.csv"
                    novo_lead = pd.DataFrame([{
                        "Data_Cadastro": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Nome": nome_cliente,
                        "Email": email_cliente,
                        "WhatsApp": whatsapp_cliente
                    }])

                    if not os.path.exists(arquivo_leads):
                        novo_lead.to_csv(arquivo_leads, index=False, sep=";", encoding="utf-8-sig")
                    else:
                        novo_lead.to_csv(arquivo_leads, mode="a", header=False, index=False, sep=";", encoding="utf-8-sig")

                    st.session_state.lead_desbloqueado = True
                    st.session_state.nome_usuario = nome_cliente
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos para liberar seu acesso.")

# =========================================================================
# MÓDULO: PAINEL ADMINISTRATIVO COM SENHA (NOVIDADE)
# =========================================================================
if st.session_state.modulo_atual == "🔒 Painel Admin (Leads)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🔒 Backoffice do Administrador - Gestão de Leads</h3>", unsafe_allow_html=True)
    st.caption("Área restrita para visualização, auditoria e download dos contatos capturados.")

    # Controle de autenticação na sessão
    if "admin_logado" not in st.session_state:
        st.session_state.admin_logado = False

    if not st.session_state.admin_logado:
        col_login, _ = st.columns([1, 2])
        with col_login:
            st.markdown("""
            <div class="metric-card" style="margin-bottom:16px;">
                <div class="metric-label" style="color:#6366f1;">Autenticação Obrigatória</div>
                <div style="font-size:0.9rem; color:#cbd5e1; margin-top:4px;">Insira a chave mestre para gerenciar a base de dados.</div>
            </div>
            """, unsafe_allow_html=True)
            
            senha_digitada = st.text_input("Senha do Administrador", type="password", placeholder="Digite sua senha...")
            if st.button("🔓 Acessar Painel de Controle"):
                if senha_digitada == admin_password:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta. Acesso negado.")
    else:
        # CONTEÚDO AUTENTICADO DO ADMINISTRADOR
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; background:#141923; padding:12px 18px; border-radius:8px; border:1px solid #6366f1; margin-bottom:20px;">
            <div>
                <span style="color:#6366f1; font-weight:700;">● MODO ADMINISTRADOR ATIVO</span>
                <span style="color:#94a3b8; font-size:0.9rem; margin-left:10px;">Gestão de Clientes Potenciais</span>
            </div>
            <span class="admin-badge">PRIVADO</span>
        </div>
        """, unsafe_allow_html=True)

        arquivo_leads = "leads_capturados.csv"

        if os.path.exists(arquivo_leads):
            try:
                df_leads = pd.read_csv(arquivo_leads, sep=";", encoding="utf-8-sig")
                total_leads = len(df_leads)

                # Cards de Métricas Administrativas
                c_adm1, c_adm2, c_adm3 = st.columns(3)
                with c_adm1:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Total de Clientes Capturados</div><div class="metric-value metric-accent">{total_leads} leads</div></div>', unsafe_allow_html=True)
                with c_adm2:
                    ultimo_cadastro = df_leads["Data_Cadastro"].iloc[-1] if total_leads > 0 else "Nenhum"
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Último Cadastro Registrado</div><div class="metric-value" style="font-size:1.15rem;">{ultimo_cadastro}</div></div>', unsafe_allow_html=True)
                with c_adm3:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Status do Banco de Dados</div><div class="metric-value metric-positive">100% Operacional</div></div>', unsafe_allow_html=True)

                st.write("")
                st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem;'>📋 Relação Completa de Clientes</h4>", unsafe_allow_html=True)

                # Botão de Exportação para Excel / CSV
                csv_bytes_leads = df_leads.to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
                
                col_btn_down, col_logout = st.columns([2, 1])
                with col_btn_down:
                    st.download_button(
                        label="⬇️ Baixar Base de Leads Completa (.CSV / Excel)",
                        data=csv_bytes_leads,
                        file_name=f"base_leads_alphabet_{datetime.date.today().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Gera arquivo pronto para importar em listas de WhatsApp, e-mail marketing ou Excel."
                    )
                with col_logout:
                    if st.button("🚪 Sair do Painel Admin"):
                        st.session_state.admin_logado = False
                        st.rerun()

                # Tabela de Clientes
                st.dataframe(df_leads, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Erro ao ler a base de dados de leads: {e}")
        else:
            st.info("Nenhum cliente cadastrado até o momento. O arquivo 'leads_capturados.csv' será gerado automaticamente assim que o primeiro visitante preencher a Ficha VIP.")
            if st.button("🚪 Sair do Painel Admin"):
                st.session_state.admin_logado = False
                st.rerun()

# =========================================================================
# MÓDULO: RADAR IN-PLAY
# =========================================================================
elif st.session_state.modulo_atual == "🔴 Radar In-Play (Ao Vivo)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🔴 Radar In-Play com Índice de Pressão (IPM)</h3>", unsafe_allow_html=True)
    st.caption("Fórmula quantitativa: [ (Chutes no Alvo x 2) + Chutes Fora + Escanteios ] / Minuto de Jogo")

    col_filtros1, col_filtros2 = st.columns(2)
    with col_filtros1:
        minuto_corte = st.slider("Minuto Mínimo de Partida", min_value=1, max_value=90, value=30)
    with col_filtros2:
        ipm_corte = st.slider("Alerta de Pressão Mínima (IPM)", min_value=0.10, max_value=0.60, value=0.30, step=0.05)

    if not api_key:
        st.warning("⚠️ Insira sua chave gratuita da API-Football nas configurações do Streamlit Cloud.")
    else:
        if st.button("🔄 Escanear Partidas e Calcular Pressão"):
            with st.spinner("Conectando à API, capturando estatísticas de chutes e calculando IPM..."):
                headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}
                try:
                    res = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers, timeout=10)
                    dados_live = res.json().get("response", [])

                    if not dados_live:
                        st.info("Nenhuma partida ao vivo no momento ou cota diária esgotada.")
                    else:
                        jogos_qualificados = 0
                        for jogo in dados_live:
                            minuto = jogo["fixture"]["status"]["elapsed"]
                            if minuto is None or minuto < minuto_corte:
                                continue

                            fixture_id = jogo["fixture"]["id"]
                            mandante = jogo["teams"]["home"]["name"]
                            visitante = jogo["teams"]["away"]["name"]
                            gols_m = jogo["goals"]["home"] or 0
                            gols_v = jogo["goals"]["away"] or 0
                            liga = jogo["league"]["name"]
                            pais = jogo["league"]["country"]

                            url_stats = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}"
                            res_stats = requests.get(url_stats, headers=headers, timeout=8)
                            dados_stats = res_stats.json().get("response", [])

                            chutes_alvo_total = 0
                            chutes_fora_total = 0
                            escanteios_total = 0

                            if dados_stats:
                                for equipe in dados_stats:
                                    for item in equipe.get("statistics", []):
                                        t = item["type"]
                                        val = item["value"] or 0
                                        if t == "Shots on Goal": chutes_alvo_total += val
                                        elif t == "Shots off Goal": chutes_fora_total += val
                                        elif t == "Corner Kicks": escanteios_total += val

                            pontuacao_pressao = (chutes_alvo_total * 2) + chutes_fora_total + escanteios_total
                            ipm = pontuacao_pressao / max(1, minuto)

                            if ipm >= ipm_corte:
                                jogos_qualificados += 1
                                tag_pressao = '<span class="live-badge">🔥 BLITZ TOTAL</span>' if ipm >= 0.35 else '<span class="vip-badge">⚡ JOGO ABERTO</span>'

                                st.markdown(f"""
                                <div class="match-card">
                                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                        <div>
                                            <span class="live-badge">AO VIVO {minuto}'</span>
                                            <span style="font-size:0.8rem; color:#94a3b8; margin-left:8px;">{pais} - {liga}</span>
                                            <div style="font-size:1.15rem; font-weight:700; margin-top:6px; color:#f8fafc;">
                                                {mandante} <span style="color:#38bdf8;">{gols_m} x {gols_v}</span> {visitante}
                                            </div>
                                        </div>
                                        <div style="text-align:right;">
                                            {tag_pressao}
                                            <div style="font-size:1.35rem; font-weight:800; color:#38bdf8; margin-top:4px;">IPM: {ipm:.2f}</div>
                                        </div>
                                    </div>
                                    <div style="display:flex; gap:20px; background:#0b0e14; padding:10px 14px; border-radius:8px; margin-top:12px; border:1px solid #232b3e;">
                                        <span style="font-size:0.85rem; color:#cbd5e1;">🎯 Chutes no Alvo: <b>{chutes_alvo_total}</b></span>
                                        <span style="font-size:0.85rem; color:#cbd5e1;">🥅 Chutes Fora: <b>{chutes_fora_total}</b></span>
                                        <span style="font-size:0.85rem; color:#cbd5e1;">🚩 Escanteios: <b>{escanteios_total}</b></span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                        if jogos_qualificados == 0:
                            st.info("Nenhuma partida ao vivo atendeu aos filtros de minuto e IPM no momento.")

                except Exception as e:
                    st.error(f"Erro ao consultar partidas: {e}")

# =========================================================================
# MÓDULOS VIP, BACKTEST, AGENDA E CALCULADORA
# =========================================================================
elif st.session_state.modulo_atual == "👑 Análises VIP (Pré-Jogo)":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Inteligência e Projeções Pré-Jogo VIP")
    else:
        usuario_ativo = st.session_state.get("nome_usuario", "Assinante")
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; background:#141923; padding:12px 18px; border-radius:8px; border:1px solid #10b981; margin-bottom:20px;">
            <div>
                <span style="color:#10b981; font-weight:700;">● MÓDULO VIP ATIVO</span>
                <span style="color:#94a3b8; font-size:0.9rem; margin-left:10px;">Bem-vindo(a), <b>{usuario_ativo}</b></span>
            </div>
            <span class="vip-badge">RELATÓRIOS LIBERADOS</span>
        </div>
        """, unsafe_allow_html=True)

        dados_analises_vip = [
            {"Partida": "Arsenal vs Chelsea", "Liga": "Premier League", "Mercado": "Over 2.5 Gols", "Odd_Mercado": 1.95, "Odd_Justa_Modelo": 1.72, "EV_Estimado": "+13.3%", "xG_Projetado": "3.10 gols", "Recomendacao": "Forte Valor no Over"},
            {"Partida": "Real Madrid vs Villarreal", "Liga": "La Liga", "Mercado": "Back Mandante", "Odd_Mercado": 1.62, "Odd_Justa_Modelo": 1.48, "EV_Estimado": "+9.4%", "xG_Projetado": "2.65 x 0.85", "Recomendacao": "Validado no Backtest 5 Anos"},
            {"Partida": "Bayer Leverkusen vs Dortmund", "Liga": "Bundesliga", "Mercado": "Ambas Marcam (BTTS)", "Odd_Mercado": 1.68, "Odd_Justa_Modelo": 1.50, "EV_Estimado": "+12.0%", "xG_Projetado": "3.45 gols", "Recomendacao": "Tendência Ofensiva Alta"}
        ]
        for item in dados_analises_vip:
            st.markdown(f"""
            <div class="match-card" style="border-left: 4px solid #f59e0b;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="vip-badge">{item['Liga']}</span>
                        <div style="font-size:1.15rem; font-weight:700; margin-top:6px; color:#f8fafc;">{item['Partida']}</div>
                        <div style="font-size:0.9rem; color:#cbd5e1; margin-top:4px;">Mercado: <b style="color:#38bdf8;">{item['Mercado']}</b> | Odd: <b>{item['Odd_Mercado']}</b> (Justa: {item['Odd_Justa_Modelo']})</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:1.3rem; font-weight:800; color:#10b981;">{item['EV_Estimado']}</div>
                        <div style="font-size:0.8rem; color:#94a3b8;">xG: {item['xG_Projetado']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.modulo_atual == "🧪 Backtest Histórico (Área VIP)":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Simulador Quantitativo de 5 Anos de Backtest")
    else:
        st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🧪 Simulador Histórico de Longo Prazo (5 Anos)</h3>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: liga_escolhida = st.selectbox("Competição", ["Premier League (Inglaterra)", "La Liga (Espanha)", "Serie A (Itália)", "Bundesliga (Alemanha)"])
        with c2: mercado = st.selectbox("Mercado Alvo", ["Over 2.5 Gols (Mais de 2.5)", "Under 2.5 Gols (Menos de 2.5)", "Back Mandante (Casa)", "Back Visitante (Fora)", "Back Empate"])
        with c3:
            odd_min = st.number_input("Odd Mínima", value=1.60, step=0.05)
            odd_max = st.number_input("Odd Máxima", value=2.20, step=0.05)
        with c4: stake_tipo = st.number_input("Stake por Entrada (R$)", min_value=10.0, value=100.0, step=10.0)

        mapa_ligas = {"Premier League (Inglaterra)": "E0", "La Liga (Espanha)": "SP1", "Serie A (Itália)": "I1", "Bundesliga (Alemanha)": "D1"}
        temporadas = [{"nome": "2019/2020", "cod": "1920"}, {"nome": "2020/2021", "cod": "2021"}, {"nome": "2021/2022", "cod": "2122"}, {"nome": "2022/2023", "cod": "2223"}, {"nome": "2023/2024", "cod": "2324"}]

        if st.button("🚀 Executar Simulação Histórica (5 Anos)"):
            barra = st.progress(0)
            dfs = []
            cod = mapa_ligas[liga_escolhida]
            for i, t in enumerate(temporadas):
                try:
                    df_t = pd.read_csv(f"https://www.football-data.co.uk/mmz4281/{t['cod']}/{cod}.csv")
                    cols = [c for c in ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'B365H', 'B365D', 'B365A', 'B365>2.5', 'B365<2.5'] if c in df_t.columns]
                    df_t = df_t[cols].dropna()
                    df_t['Temporada'] = t['nome']
                    dfs.append(df_t)
                except Exception: pass
                barra.progress((i + 1) / len(temporadas))
            barra.empty()

            if dfs:
                base = pd.concat(dfs, ignore_index=True)
                regs, lucro, pico, dd, hist = [], 0.0, 0.0, 0.0, [0.0]
                for _, r in base.iterrows():
                    if mercado == "Over 2.5 Gols (Mais de 2.5)":
                        if 'B365>2.5' not in r: continue
                        odd = r['B365>2.5']; win = (r['FTHG'] + r['FTAG']) > 2.5
                    elif mercado == "Under 2.5 Gols (Menos de 2.5)":
                        if 'B365<2.5' not in r: continue
                        odd = r['B365<2.5']; win = (r['FTHG'] + r['FTAG']) < 2.5
                    elif mercado == "Back Mandante (Casa)": odd = r.get('B365H', 0); win = (r['FTR'] == 'H')
                    elif mercado == "Back Visitante (Fora)": odd = r.get('B365A', 0); win = (r['FTR'] == 'A')
                    else: odd = r.get('B365D', 0); win = (r['FTR'] == 'D')

                    if odd_min <= odd <= odd_max:
                        res = (odd - 1.0) * stake_tipo if win else -stake_tipo
                        lucro += res
                        hist.append(lucro)
                        if lucro > pico: pico = lucro
                        if (pico - lucro) > dd: dd = pico - lucro
                        regs.append({"Data": r['Date'], "Temporada": r['Temporada'], "Partida": f"{r['HomeTeam']} vs {r['AwayTeam']}", "Placar": f"{int(r['FTHG'])}x{int(r['FTAG'])}", "Odd": odd, "Status": "GREEN" if win else "RED", "Resultado_R$": round(res, 2), "Acerto": 1 if win else 0, "Volume": stake_tipo})

                if regs:
                    df_res = pd.DataFrame(regs)
                    st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-top:20px;'>📊 Performance da Estratégia (5 Anos)</h4>", unsafe_allow_html=True)
                    m1, m2, m3, m4, m5 = st.columns(5)
                    wr = (df_res['Acerto'].sum() / len(df_res)) * 100
                    roi = (lucro / (len(df_res) * stake_tipo)) * 100
                    lc = "metric-positive" if lucro >= 0 else "metric-negative"
                    m1.markdown(f'<div class="metric-card"><div class="metric-label">Amostra</div><div class="metric-value metric-accent">{len(df_res)} jogos</div></div>', unsafe_allow_html=True)
                    m2.markdown(f'<div class="metric-card"><div class="metric-label">Win Rate</div><div class="metric-value">{wr:.1f}%</div></div>', unsafe_allow_html=True)
                    m3.markdown(f'<div class="metric-card"><div class="metric-label">Lucro Líquido</div><div class="metric-value {lc}">R$ {lucro:,.2f}</div></div>', unsafe_allow_html=True)
                    m4.markdown(f'<div class="metric-card"><div class="metric-label">ROI Global</div><div class="metric-value {lc}">{roi:.2f}%</div></div>', unsafe_allow_html=True)
                    m5.markdown(f'<div class="metric-card"><div class="metric-label">Max Drawdown</div><div class="metric-value metric-negative">-R$ {dd:,.2f}</div></div>', unsafe_allow_html=True)

                    fig_curva = go.Figure(go.Scatter(x=list(range(len(hist))), y=hist, mode='lines', line=dict(color='#38bdf8', width=2.5), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.08)'))
                    fig_curva.update_layout(title="<b>Curva de Patrimônio Líquido</b>", paper_bgcolor='#0b0e14', plot_bgcolor='#141923', font=dict(color='#94a3b8'), height=340)
                    st.plotly_chart(fig_curva, use_container_width=True)

                    csv_b = df_res.drop(columns=['Acerto', 'Volume']).to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
                    st.download_button("⬇️ Baixar Auditoria (.CSV / Excel)", data=csv_b, file_name=f"audit_5anos_{cod}.csv", mime="text/csv")

elif st.session_state.modulo_atual == "📅 Agenda (Próximos Jogos)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>📅 Agenda de Jogos do Dia</h3>", unsafe_allow_html=True)
    if api_key:
        hoje = datetime.date.today().strftime("%Y-%m-%d")
        if st.button("📅 Carregar Grade do Dia"):
            res = requests.get(f"https://v3.football-data.api-sports.io/fixtures?date={hoje}", headers={"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}, timeout=10)
            jogos = res.json().get("response", [])
            for j in jogos[:25]:
                st.markdown(f"""
                <div class="match-card">
                    <span style="color:#38bdf8; font-weight:700;">⏰ {j['fixture']['date'][11:16]} UTC</span> | {j['league']['country']} - {j['league']['name']}: <b>{j['teams']['home']['name']} vs {j['teams']['away']['name']}</b>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.modulo_atual == "🧮 Calculadora de Valor (+EV)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🧮 Precificação Precisa & Gestão de Risco</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        odd = st.number_input("Odd Oferecida", min_value=1.01, value=2.00, step=0.05)
        prob = st.slider("Probabilidade Estimada (%)", min_value=1, max_value=99, value=55)
        banca = st.number_input("Capital da Banca (R$)", min_value=10.0, value=1000.0, step=50.0)
    with c2:
        prob_dec = prob / 100.0
        ev = (prob_dec * (odd - 1.0)) - (1.0 - prob_dec)
        st.metric("Odd Justa", f"{(1.0/prob_dec):.2f}")
        st.metric("Margem de Valor (+EV)", f"{ev*100:.1f}%")
        if ev > 0:
            st.success(f"✅ ENTRADA COM VALOR MATEMÁTICO! Stake 1/4 Kelly: R$ {max(0.0, (((odd-1.0)*prob_dec - (1.0-prob_dec))/(odd-1.0)/4.0)*banca):.2f}")
        else:
            st.error("❌ Aposta sem valor esperado positivo.")
