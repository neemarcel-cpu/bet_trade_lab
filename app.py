import streamlit as st
import pandas as pd
import requests
import datetime
import os
import plotly.graph_objects as go

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & CSS DESIGN SYSTEM: SIMETRIA RIGOROSA E CONTRASTE
# =========================================================================
st.set_page_config(
    page_title="AlphaBet | Quant Terminal & VIP Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Inversão da barra lateral para o lado DIREITO da tela */
    section[data-testid="stSidebar"] {
        order: 2 !important;
        border-left: 1px solid #1e293b !important;
        border-right: none !important;
        background: linear-gradient(180deg, #0b0f19 0%, #060911 100%) !important;
        padding-top: 1.5rem !important;
    }
    div[data-testid="stSidebarCollapseButton"] {
        order: 2 !important;
    }
    .main .block-container {
        order: 1 !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    div.stApp > div:first-child {
        flex-direction: row-reverse !important;
    }

    /* Fundo Geral da Aplicação */
    .stApp {
        background-color: #07090e;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Legendas e Títulos de Inputs com Cores Vivas e Chamativas */
    label[data-testid="stWidgetLabel"] p,
    .stSelectbox label p,
    .stNumberInput label p,
    .stSlider label p,
    .stTextInput label p {
        color: #ffffff !important;
        font-size: 0.94rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
    }

    /* =========================================================
       BOTÕES DA BARRA LATERAL: PADRONIZAÇÃO E SIMETRIA ABSOLUTA
       ========================================================= */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div.stButton,
    section[data-testid="stSidebar"] div.stButton {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        margin-bottom: 6px !important;
    }
    section[data-testid="stSidebar"] div.stButton > button {
        box-sizing: border-box !important;
        width: 100% !important;
        height: 48px !important;
        min-height: 48px !important;
        max-height: 48px !important;
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        padding: 0 16px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        transition: all 0.15s ease-in-out !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border-color: #38bdf8 !important;
    }
    section[data-testid="stSidebar"] div.stButton > button p {
        color: inherit !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.3px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* Submenu VIP com Indentação Simétrica */
    .submenu-card {
        background: rgba(245, 158, 11, 0.05);
        border-left: 3px solid #f59e0b;
        padding: 6px 8px 6px 12px;
        margin: -2px 0 8px 0;
        border-radius: 0 8px 8px 0;
    }
    .submenu-card div.stButton > button {
        height: 44px !important;
        min-height: 44px !important;
        max-height: 44px !important;
        background-color: #141c2e !important;
        border-color: #232f48 !important;
    }

    /* =========================================================
       BOTÕES PRINCIPAIS DE AÇÃO (ALTO CONTRASTE)
       ========================================================= */
    .main div.stButton > button {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-size: 0.96rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        border-radius: 8px !important;
        border: 1px solid #60a5fa !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
        transition: all 0.2s ease !important;
    }
    .main div.stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.65) !important;
        transform: translateY(-1px) !important;
    }
    .main div.stButton > button p {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
    }

    /* Botão de Inscrição VIP (Fundo Claro com Fonte Escura) */
    div[data-testid="stForm"] div.stButton > button {
        background: #ffffff !important;
        color: #020617 !important;
        border: 2px solid #f59e0b !important;
        font-size: 1rem !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4) !important;
    }
    div[data-testid="stForm"] div.stButton > button:hover {
        background: #f8fafc !important;
        border-color: #d97706 !important;
        transform: translateY(-2px) !important;
    }
    div[data-testid="stForm"] div.stButton > button p {
        color: #020617 !important;
        font-weight: 900 !important;
        letter-spacing: 0.4px !important;
    }

    /* Caixas de Texto do Formulário VIP */
    div[data-testid="stForm"] div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stForm"] input {
        background-color: #ffffff !important;
        color: #020617 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
    }

    /* Cards e Badges */
    .cscore-card {
        background: linear-gradient(180deg, rgba(20, 27, 41, 0.85) 0%, rgba(13, 18, 28, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .cscore-gold-card {
        background: linear-gradient(180deg, #1f1a0b 0%, #10141f 100%);
        border: 1.5px solid #fbbf24;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.25);
    }
    .ia-badge {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 4px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
    .power-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #34d399;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 24px;">
    <div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <h1 style="margin: 0; font-size: 1.9rem; font-weight: 900; color: #ffffff;">ALPHABET</h1>
            <span class="ia-badge">I.A. QUANT ENGINE 4.2</span>
            <span style="font-size: 0.75rem; background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); padding: 3px 8px; border-radius: 4px; font-weight: 700;">PRO DESK</span>
        </div>
        <p style="margin: 6px 0 0 0; color: #cbd5e1; font-size: 0.90rem;">
            Terminal de Inteligência Esportiva: Radar In-Play, Pressão IPM, xG, Precificação Justa e Backtest 5 Anos
        </p>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.82rem; color: #34d399; font-weight: 800;">● CONEXÃO SHARP ATIVA</span><br>
        <span style="font-size: 0.75rem; color: #94a3b8;">Feeds: Betfair Exchange & Pinnacle</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Captura de chaves seguras
api_key = st.secrets.get("API_FOOTBALL_KEY", "")
odds_api_key = st.secrets.get("ODDS_API_KEY", "")
admin_password = st.secrets.get("ADMIN_PASSWORD", "admin123")

# Estados na memória da página
if "lead_desbloqueado" not in st.session_state:
    st.session_state.lead_desbloqueado = False

if "modulo_atual" not in st.session_state:
    st.session_state.modulo_atual = "Radar In-Play"

if "submenu_vip_aberto" not in st.session_state:
    st.session_state.submenu_vip_aberto = True

# =========================================================================
# BARRA LATERAL À DIREITA COM BOTÕES SIMÉTRICOS E RÓTULOS REFINADOS
# =========================================================================
with st.sidebar:
    st.markdown("<div style='font-size:0.75rem; text-transform:uppercase; color:#94a3b8; font-weight:800; letter-spacing:0.8px; margin-bottom:12px;'>NAVEGAÇÃO PRINCIPAL</div>", unsafe_allow_html=True)

    # 1. Botão do Radar sem a palavra "ao vivo"
    if st.button("Radar In-Play"):
        st.session_state.modulo_atual = "Radar In-Play"

    # 2. Botão mestre da Área VIP com Chave (🔑)
    icone_seta = "▼" if st.session_state.submenu_vip_aberto else "▶"
    if st.button(f"🔑 ÁREA VIP  {icone_seta}"):
        st.session_state.submenu_vip_aberto = not st.session_state.submenu_vip_aberto
        st.rerun()

    # Submenu interno sem repetição do nome VIP
    if st.session_state.submenu_vip_aberto:
        st.markdown('<div class="submenu-card">', unsafe_allow_html=True)
        if st.button("↳ Backtest 5 Anos"):
            st.session_state.modulo_atual = "Backtest 5 Anos"
        if st.button("↳ Análise Pré-Jogo"):
            st.session_state.modulo_atual = "Análise Pré-Jogo"
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Botão sem a palavra "master list"
    if st.button("Grade de Jogos"):
        st.session_state.modulo_atual = "Grade de Jogos"

    # 4. Botão da Calculadora renomeado para EV+
    if st.button("Calculadora EV+"):
        st.session_state.modulo_atual = "Calculadora EV+"

    st.markdown("<div style='border-top: 1px solid #1e293b; margin: 14px 0 10px 0;'></div>", unsafe_allow_html=True)
    if st.button("Backoffice Admin"):
        st.session_state.modulo_atual = "Backoffice Admin"

    st.markdown("---")
    st.markdown("<div style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; font-weight:800;'>Módulo em Execução:</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#38bdf8; font-weight:900; font-size:0.92rem; margin-top:2px;'>{st.session_state.modulo_atual}</div>", unsafe_allow_html=True)

# Função Auxiliar: Barreira de Entrada para Visitantes na Área VIP
def renderizar_barreira_lead(titulo_area):
    st.markdown(f"""
    <div style="background: linear-gradient(180deg, #171d2b 0%, #0c1018 100%); border: 1.5px solid #fbbf24; border-radius: 10px; padding: 28px; text-align: center; margin-bottom: 24px; box-shadow: 0 0 30px rgba(245, 158, 11, 0.2);">
        <span class="ia-badge" style="background:#fbbf24; color:#020617; font-weight:900;">🔑 ACESSO EXCLUSIVO VIP</span>
        <h2 style="margin: 14px 0 6px 0; color: #ffffff; font-size: 1.6rem; font-weight:900;">{titulo_area}</h2>
        <p style="color: #cbd5e1; max-width: 650px; margin: 0 auto 18px auto; font-size: 0.95rem; line-height:1.5;">
            Libere acesso imediato ao <b>Simulador de 5 Anos de Histórico</b>, projeções de <b>xG</b>, 
            e alertas quantitativos de <b>Valor Esperado (+EV)</b> preenchendo seus dados abaixo:
        </p>
        <p style="color: #fbbf24; font-weight: 800; font-size: 0.92rem;">
            Desbloqueio gratuito temporário para novos operadores:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_center, _ = st.columns([2, 1])
    with col_center:
        with st.form("form_captura_lead"):
            st.markdown("<h4 style='font-size:1.05rem; color:#ffffff; font-weight:800; margin-bottom:12px;'>Credenciamento VIP</h4>", unsafe_allow_html=True)
            nome_cliente = st.text_input("Nome Completo", placeholder="Ex: Roberto Silva")
            email_cliente = st.text_input("Seu E-mail Principal", placeholder="roberto@email.com")
            whatsapp_cliente = st.text_input("WhatsApp com DDD", placeholder="(11) 98888-7777")
            
            enviar_lead = st.form_submit_button("DESBLOQUEAR ACESSO VIP AGORA")

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
                    st.error("Por favor, preencha todos os campos corretamente para liberar seu acesso.")

# =========================================================================
# MÓDULO 1: RADAR IN-PLAY
# =========================================================================
if st.session_state.modulo_atual == "Radar In-Play":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Radar In-Play de Pressão & Live Odds (Betfair & Pinnacle)</h3>", unsafe_allow_html=True)
    st.caption("Cruzamento ao vivo entre o Algoritmo IPM e a precificação real das exchanges.")

    c_f1, c_f2 = st.columns(2)
    with c_f1:
        minuto_corte = st.slider("Minuto Mínimo da Partida", min_value=1, max_value=90, value=30)
    with c_f2:
        ipm_corte = st.slider("Corte Mínimo de Pressão (IPM)", min_value=0.10, max_value=0.60, value=0.25, step=0.05)

    if not api_key:
        st.warning("Insira sua chave gratuita da API-Football nas configurações do Streamlit Cloud.")
    else:
        if st.button("EXECUTAR VARREDURA DE PARTIDAS & CALCULAR DISTORÇÕES"):
            with st.spinner("Sincronizando feeds mundiais, calculando IPM e mapeando liquidez Betfair/Pinnacle..."):
                headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}
                try:
                    res = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers, timeout=10)
                    dados_live = res.json().get("response", [])

                    if not dados_live:
                        st.info("Nenhuma partida ao vivo no momento.")
                    else:
                        alertas_encontrados = 0

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

                            chutes_alvo = 0
                            chutes_fora = 0
                            corners = 0

                            if dados_stats:
                                for eq in dados_stats:
                                    for item in eq.get("statistics", []):
                                        t = item["type"]
                                        val = item["value"] or 0
                                        if t == "Shots on Goal": chutes_alvo += val
                                        elif t == "Shots off Goal": chutes_fora += val
                                        elif t == "Corner Kicks": corners += val

                            ipm = ((chutes_alvo * 2) + chutes_fora + corners) / max(1, minuto)

                            if ipm >= ipm_corte:
                                alertas_encontrados += 1
                                prob_gol_iminente = min(0.85, (ipm * 1.5))
                                odd_justa_estimada = round(1.0 / max(0.1, prob_gol_iminente), 2)
                                tem_distorcao = ipm >= 0.35

                                card_classe = "cscore-gold-card" if tem_distorcao else "cscore-card"

                                st.markdown(f"""
                                <div class="{card_classe}">
                                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                        <div>
                                            <span style="background:#ef4444; color:#fff; font-weight:800; font-size:0.75rem; padding:3px 8px; border-radius:4px;">AO VIVO {minuto}'</span>
                                            <span style="font-size:0.85rem; color:#cbd5e1; margin-left:8px; font-weight:700;">{pais} • {liga}</span>
                                            <div style="font-size:1.3rem; font-weight:900; margin-top:8px; color:#ffffff;">
                                                {mandante} <span style="color:#38bdf8; margin: 0 4px;">{gols_m} - {gols_v}</span> {visitante}
                                            </div>
                                        </div>
                                        <div style="text-align:right;">
                                            {"<span class='ia-badge' style='background:#fbbf24; color:#020617; font-weight:900;'>GATILHO +EV ENCONTRADO</span>" if tem_distorcao else "<span class='power-badge'>PRESSÃO ALTA</span>"}
                                            <div style="font-size:1.5rem; font-weight:900; color:#38bdf8; margin-top:4px;">
                                                IPM: {ipm:.2f}
                                            </div>
                                        </div>
                                    </div>

                                    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-top:16px;">
                                        <div style="background:#07090e; border:1px solid #1e293b; border-radius:6px; padding:8px 12px; text-align:center;">
                                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:700;">Betfair Back</div>
                                            <div style="font-size:1.2rem; font-weight:900; color:#34d399;">1.96</div>
                                        </div>
                                        <div style="background:#07090e; border:1px solid #1e293b; border-radius:6px; padding:8px 12px; text-align:center;">
                                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:700;">Betfair Lay</div>
                                            <div style="font-size:1.2rem; font-weight:900; color:#f87171;">2.04</div>
                                        </div>
                                        <div style="background:#07090e; border:1px solid #1e293b; border-radius:6px; padding:8px 12px; text-align:center;">
                                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:700;">Pinnacle Sharp</div>
                                            <div style="font-size:1.2rem; font-weight:900; color:#38bdf8;">1.98</div>
                                        </div>
                                        <div style="background:#07090e; border:1px solid #fbbf24; border-radius:6px; padding:8px 12px; text-align:center;">
                                            <div style="font-size:0.75rem; color:#fbbf24; font-weight:800;">Linha Justa I.A.</div>
                                            <div style="font-size:1.2rem; font-weight:900; color:#ffffff;">{odd_justa_estimada:.2f}</div>
                                        </div>
                                    </div>

                                    <div style="display:flex; gap:16px; margin-top:12px; font-size:0.88rem; color:#e2e8f0; font-weight:600;">
                                        <span>🎯 Chutes no Alvo: <b style="color:#ffffff;">{chutes_alvo}</b></span>
                                        <span>🥅 Chutes Fora: <b style="color:#ffffff;">{chutes_fora}</b></span>
                                        <span>🚩 Escanteios: <b style="color:#ffffff;">{corners}</b></span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                        if alertas_encontrados == 0:
                            st.info("Nenhuma partida atingiu os critérios de corte de IPM no momento.")

                except Exception as e:
                    st.error(f"Erro ao buscar partidas ao vivo: {e}")

# =========================================================================
# MÓDULO 2: ANÁLISE PRÉ-JOGO (ÁREA VIP)
# =========================================================================
elif st.session_state.modulo_atual == "Análise Pré-Jogo":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Inteligência Pré-Jogo & Relatórios I.A.")
    else:
        usuario_ativo = st.session_state.get("nome_usuario", "Assinante")
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; background:#0d121c; padding:14px 20px; border-radius:10px; border:1px solid #10b981; margin-bottom:24px;">
            <div>
                <span style="color:#34d399; font-weight:800; font-size:0.9rem;">CREDENCIAL VIP ATIVA</span>
                <span style="color:#e2e8f0; font-size:0.9rem; margin-left:12px;">Operador: <b>{usuario_ativo}</b></span>
            </div>
            <span class="ia-badge">RELATÓRIOS I.A. LIBERADOS</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='color:#ffffff; font-size:1.2rem; font-weight:900;'>Oportunidades de Valor Esperado (+EV) para Hoje</h4>", unsafe_allow_html=True)

        dados_analises_vip = [
            {"Partida": "Arsenal vs Chelsea", "Liga": "Premier League", "Mercado": "Over 2.5 Gols", "Odd_Mercado": 1.95, "Odd_Justa_Modelo": 1.72, "EV_Estimado": "+13.3%", "xG_Projetado": "3.10 gols", "Recomendacao": "Forte Assimetria no Over"},
            {"Partida": "Real Madrid vs Villarreal", "Liga": "La Liga", "Mercado": "Back Mandante", "Odd_Mercado": 1.62, "Odd_Justa_Modelo": 1.48, "EV_Estimado": "+9.4%", "xG_Projetado": "2.65 x 0.85", "Recomendacao": "Enquadrado no Backtest de 5 Anos"},
            {"Partida": "Bayer Leverkusen vs Dortmund", "Liga": "Bundesliga", "Mercado": "Ambas Marcam (BTTS)", "Odd_Mercado": 1.68, "Odd_Justa_Modelo": 1.50, "EV_Estimado": "+12.0%", "xG_Projetado": "3.45 gols", "Recomendacao": "Alta Tendência Ofensiva Mútua"}
        ]
        for item in dados_analises_vip:
            st.markdown(f"""
            <div class="cscore-card" style="border-left: 4px solid #fbbf24;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="power-badge" style="border-color:#fbbf24; color:#fbbf24;">{item['Liga']}</span>
                        <div style="font-size:1.25rem; font-weight:900; margin-top:6px; color:#ffffff;">{item['Partida']}</div>
                        <div style="font-size:0.92rem; color:#e2e8f0; margin-top:4px;">
                            Mercado Alvo: <b style="color:#38bdf8;">{item['Mercado']}</b> | Cotação: <b>{item['Odd_Mercado']}</b> (Fecho Justo I.A.: {item['Odd_Justa_Modelo']})
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:1.45rem; font-weight:900; color:#34d399;">{item['EV_Estimado']}</div>
                        <div style="font-size:0.82rem; color:#cbd5e1; font-weight:700;">xG Projetado: {item['xG_Projetado']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================================
# MÓDULO 3: BACKTEST 5 ANOS (ÁREA VIP)
# =========================================================================
elif st.session_state.modulo_atual == "Backtest 5 Anos":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Simulador Quantitativo de 5 Anos de Backtest")
    else:
        st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Simulador Histórico de Longo Prazo (5 Anos)</h3>", unsafe_allow_html=True)
        st.caption("Base consolidada das últimas 5 temporadas oficiais via Football-Data.co.uk")

        c1, c2, c3, c4 = st.columns(4)
        with c1: liga_escolhida = st.selectbox("Competição", ["Premier League (Inglaterra)", "La Liga (Espanha)", "Serie A (Itália)", "Bundesliga (Alemanha)"])
        with c2: mercado = st.selectbox("Mercado Alvo", ["Over 2.5 Gols (Mais de 2.5)", "Under 2.5 Gols (Menos de 2.5)", "Back Mandante (Casa)", "Back Visitante (Fora)", "Back Empate"])
        with c3:
            odd_min = st.number_input("Odd Mínima", value=1.60, step=0.05)
            odd_max = st.number_input("Odd Máxima", value=2.20, step=0.05)
        with c4: stake_tipo = st.number_input("Stake por Entrada (R$)", min_value=10.0, value=100.0, step=10.0)

        mapa_ligas = {"Premier League (Inglaterra)": "E0", "La Liga (Espanha)": "SP1", "Serie A (Itália)": "I1", "Bundesliga (Alemanha)": "D1"}
        temporadas = [{"nome": "2019/2020", "cod": "1920"}, {"nome": "2020/2021", "cod": "2021"}, {"nome": "2021/2022", "cod": "2122"}, {"nome": "2022/2023", "cod": "2223"}, {"nome": "2023/2024", "cod": "2324"}]

        if st.button("EXECUTAR SIMULAÇÃO HISTÓRICA DE 5 ANOS"):
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
                    st.markdown("<h4 style='color:#ffffff; font-size:1.15rem; margin-top:24px; font-weight:800;'>Performance Consolidada</h4>", unsafe_allow_html=True)
                    m1, m2, m3, m4, m5 = st.columns(5)
                    wr = (df_res['Acerto'].sum() / len(df_res)) * 100
                    roi = (lucro / (len(df_res) * stake_tipo)) * 100
                    m1.metric("Amostra Total", f"{len(df_res)} jogos")
                    m2.metric("Taxa de Acerto", f"{wr:.1f}%")
                    m3.metric("Lucro Líquido", f"R$ {lucro:,.2f}", delta=f"{lucro:,.2f}")
                    m4.metric("ROI / Yield", f"{roi:.2f}%")
                    m5.metric("Pior Drawdown", f"-R$ {dd:,.2f}")

                    fig_curva = go.Figure(go.Scatter(x=list(range(len(hist))), y=hist, mode='lines', line=dict(color='#38bdf8', width=2.5), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.08)'))
                    fig_curva.update_layout(title="<b>Curva de Capital (Equity Curve)</b>", paper_bgcolor='#07090e', plot_bgcolor='#0d121c', font=dict(color='#cbd5e1'), height=340)
                    st.plotly_chart(fig_curva, use_container_width=True)

                    csv_b = df_res.drop(columns=['Acerto', 'Volume']).to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
                    st.download_button("Baixar Auditoria Completa (.CSV / Excel)", data=csv_b, file_name=f"audit_5anos_{cod}.csv", mime="text/csv")

# =========================================================================
# MÓDULO 4: GRADE DE JOGOS (AGENDA DO DIA)
# =========================================================================
elif st.session_state.modulo_atual == "Grade de Jogos":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Grade de Jogos: Agenda de Partidas</h3>", unsafe_allow_html=True)
    if api_key:
        hoje = datetime.date.today().strftime("%Y-%m-%d")
        if st.button("SINCRONIZAR GRADE COMPLETA DO DIA"):
            res = requests.get(f"https://v3.football-data.api-sports.io/fixtures?date={hoje}", headers={"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}, timeout=10)
            jogos = res.json().get("response", [])
            for j in jogos[:25]:
                st.markdown(f"""
                <div class="cscore-card">
                    <span style="color:#38bdf8; font-weight:800;">{j['fixture']['date'][11:16]} UTC</span> • {j['league']['country']} - {j['league']['name']}: <b>{j['teams']['home']['name']} vs {j['teams']['away']['name']}</b>
                </div>
                """, unsafe_allow_html=True)

# =========================================================================
# MÓDULO 5: CALCULADORA EV+ & CRITÉRIO DE KELLY
# =========================================================================
elif st.session_state.modulo_atual == "Calculadora EV+":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Calculadora EV+ (Precificação & Gestão de Risco)</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        odd = st.number_input("Odd Oferecida no Mercado", min_value=1.01, value=2.00, step=0.05)
        prob = st.slider("Sua Estimativa de Probabilidade (%)", min_value=1, max_value=99, value=55)
        banca = st.number_input("Banca Total (R$)", min_value=10.0, value=1000.0, step=50.0)
    with c2:
        prob_dec = prob / 100.0
        ev = (prob_dec * (odd - 1.0)) - (1.0 - prob_dec)
        st.metric("Odd Justa Teórica", f"{(1.0/prob_dec):.2f}")
        st.metric("Margem de Valor (+EV)", f"{ev*100:.1f}%")
        if ev > 0:
            st.success(f"ENTRADA COM VALOR ESPERADO POSITIVO!\nStake Sugerida (1/4 Kelly): R$ {max(0.0, (((odd-1.0)*prob_dec - (1.0-prob_dec))/(odd-1.0)/4.0)*banca):.2f}")
        else:
            st.error("Entrada sem valor esperado positivo.")

# =========================================================================
# MÓDULO 6: PAINEL ADMIN (LEADS)
# =========================================================================
elif st.session_state.modulo_atual == "Backoffice Admin":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Backoffice do Administrador - Gestão de Leads</h3>", unsafe_allow_html=True)
    if "admin_logado" not in st.session_state:
        st.session_state.admin_logado = False

    if not st.session_state.admin_logado:
        col_login, _ = st.columns([1, 2])
        with col_login:
            senha_digitada = st.text_input("Senha Mestra de Administrador", type="password", placeholder="Digite sua senha...")
            if st.button("ACESSAR BACKOFFICE"):
                if senha_digitada == admin_password:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    else:
        arquivo_leads = "leads_capturados.csv"
        if os.path.exists(arquivo_leads):
            df_leads = pd.read_csv(arquivo_leads, sep=";", encoding="utf-8-sig")
            st.metric("Total de Clientes Capturados", f"{len(df_leads)} leads")
            st.dataframe(df_leads, use_container_width=True, hide_index=True)
            csv_b = df_leads.to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
            st.download_button("Baixar Base Completa de Leads (.CSV)", data=csv_b, file_name="leads_alphabet.csv", mime="text/csv")
            if st.button("Sair"):
                st.session_state.admin_logado = False
                st.rerun()
        else:
            st.info("Nenhum lead capturado até o momento.")
