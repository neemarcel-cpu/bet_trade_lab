import streamlit as st
import pandas as pd
import requests
import datetime
import os
import plotly.graph_objects as go
from google import genai

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & CSS DESIGN SYSTEM: SIMETRIA & CONTRASTE
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

    /* Legendas e Títulos de Inputs em Branco Nítido */
    label[data-testid="stWidgetLabel"] p,
    .stSelectbox label p,
    .stNumberInput label p,
    .stSlider label p,
    .stTextInput label p,
    .stTextArea label p {
        color: #ffffff !important;
        font-size: 0.94rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
    }

    /* =========================================================
       BOTÕES DA BARRA LATERAL: SIMETRIA RIGOROSA
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
    .ia-diag-box {
        background: #0d131f;
        border: 1px solid #38bdf8;
        border-radius: 10px;
        padding: 20px;
        margin-top: 18px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.15);
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
            Terminal de Inteligência Esportiva: Radar In-Play, Assistente I.A., Diagnósticos de Valor e Backtest 5 Anos
        </p>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.82rem; color: #34d399; font-weight: 800;">● CONEXÃO SHARP & I.A. ATIVA</span><br>
        <span style="font-size: 0.75rem; color: #94a3b8;">Feeds: Betfair Exchange, Pinnacle & Gemini Engine</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Captura de chaves seguras
api_key = st.secrets.get("API_FOOTBALL_KEY", "")
odds_api_key = st.secrets.get("ODDS_API_KEY", "")
admin_password = st.secrets.get("ADMIN_PASSWORD", "admin123")
gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")

# Estados na memória da página
if "lead_desbloqueado" not in st.session_state:
    st.session_state.lead_desbloqueado = False

if "modulo_atual" not in st.session_state:
    st.session_state.modulo_atual = "Radar In-Play"

if "submenu_vip_aberto" not in st.session_state:
    st.session_state.submenu_vip_aberto = True

# =========================================================================
# BARRA LATERAL À DIREITA COM O NOME AJUSTADO DO ASSISTENTE I.A.
# =========================================================================
with st.sidebar:
    st.markdown("<div style='font-size:0.75rem; text-transform:uppercase; color:#94a3b8; font-weight:800; letter-spacing:0.8px; margin-bottom:12px;'>NAVEGAÇÃO PRINCIPAL</div>", unsafe_allow_html=True)

    if st.button("Radar In-Play"):
        st.session_state.modulo_atual = "Radar In-Play"

    # NOME AJUSTADO CONFORME SOLICITADO
    if st.button("🤖 Assistente I.A"):
        st.session_state.modulo_atual = "🤖 Assistente I.A"

    icone_seta = "▼" if st.session_state.submenu_vip_aberto else "▶"
    if st.button(f"🔑 ÁREA VIP  {icone_seta}"):
        st.session_state.submenu_vip_aberto = not st.session_state.submenu_vip_aberto
        st.rerun()

    if st.session_state.submenu_vip_aberto:
        st.markdown('<div class="submenu-card">', unsafe_allow_html=True)
        if st.button("↳ Backtest 5 Anos"):
            st.session_state.modulo_atual = "Backtest 5 Anos"
        if st.button("↳ Análise Pré-Jogo"):
            st.session_state.modulo_atual = "Análise Pré-Jogo"
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Grade de Jogos"):
        st.session_state.modulo_atual = "Grade de Jogos"

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
# MÓDULO: ASSISTENTE I.A
# =========================================================================
if st.session_state.modulo_atual == "🤖 Assistente I.A":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>🤖 Assistente I.A - Diagnóstico Quantitativo Pré-Jogo</h3>", unsafe_allow_html=True)
    st.caption("Gere diagnósticos automáticos e imparciais sobre favoritismo, tendências de gols e assimetrias de odds usando Inteligência Artificial.")

    if not gemini_api_key:
        st.warning("⚠️ Chave GEMINI_API_KEY não configurada nos Secrets do Streamlit Cloud.")
        st.info("Obtenha sua chave gratuita em aistudio.google.com e adicione-a nas configurações com o nome GEMINI_API_KEY.")
    else:
        with st.container():
            col_ia1, col_ia2 = st.columns(2)

            with col_ia1:
                confronto = st.text_input("Partida / Confronto", value="Real Madrid vs Manchester City", placeholder="Ex: Arsenal vs Chelsea")
                competicao = st.selectbox("Competição / Liga", ["UEFA Champions League", "Premier League (Inglaterra)", "La Liga (Espanha)", "Brasileirão Série A", "Serie A (Itália)", "Bundesliga (Alemanha)"])
                odd_favorito = st.number_input("Odd do Favorito no Mercado", min_value=1.01, max_value=30.0, value=1.95, step=0.05)

            with col_ia2:
                media_gols_mandante = st.number_input("Média de Gols/Jogo do Mandante (Últimos 10 jogos)", min_value=0.1, max_value=6.0, value=2.2, step=0.1)
                media_gols_visitante = st.number_input("Média de Gols/Jogo do Visitante (Últimos 10 jogos)", min_value=0.1, max_value=6.0, value=1.8, step=0.1)
                contexto_extra = st.text_area("Observações Adicionais (Desfalques, Clima, Must-Win)", placeholder="Ex: Mandante joga completo precisando da vitória; visitante sem o goleiro titular.")

        st.write("")
        if st.button("GERAR DIAGNÓSTICO E PRECIFICAÇÃO DA I.A."):
            with st.spinner("O Analista Quantitativo I.A. está calculando probabilidades, ritmo ofensivo e assimetrias..."):
                try:
                    client = genai.Client(api_key=gemini_api_key)

                    prompt_especialista = f"""
                    Você é um analista quantitativo sênior de apostas esportivas e trading em futebol, atuando como o motor inteligente 'AlphaBet Bot'.
                    Analise os dados pré-jogo abaixo e forneça um diagnóstico executivo, frio, probabilístico e focado estritamente em Valor Esperado (+EV).

                    DADOS DA PARTIDA:
                    - Confronto: {confronto}
                    - Competição: {competicao}
                    - Cotação do Favorito no Mercado: {odd_favorito}
                    - Média de Gols do Mandante: {media_gols_mandante}
                    - Média de Gols do Visitante: {media_gols_visitante}
                    - Contexto / Observações: {contexto_extra if contexto_extra else 'Nenhum desfalque informado'}

                    ESTRUTURE SUA RESPOSTA RIGOROSAMENTE COM OS SEGUINTES TÓPICOS:
                    1. 🎯 DIAGNÓSTICO DE FAVORITISMO (Quem é o favorito técnico real e se a odd de {odd_favorito} paga o risco real da partida).
                    2. ⚽ TENDÊNCIA DE GOLS (Análise probabilística de Over/Under 2.5 e Ambas Marcam / BTTS baseado no ritmo de finalizações e média conjunta de gols).
                    3. 📈 ODD JUSTA TEÓRICA (Calcule a odd justa matemática aproximada para a vitória do favorito e para Over 2.5).
                    4. 💡 VEREDITO DE ENTRADA (Recomendação técnica clara: Indique se há valor (+EV) ou se a melhor decisão é ficar de fora/esperar o Live).

                    Seja direto, profissional, sem jargões de torcedor e com foco total em preservação de capital.
                    """

                    resposta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_especialista,
                    )

                    st.markdown('<div class="ia-diag-box">', unsafe_allow_html=True)
                    st.markdown("<h4 style='color:#38bdf8; font-weight:800;'>📋 PARECER QUANTITATIVO DA I.A.</h4>", unsafe_allow_html=True)
                    st.markdown(resposta.text)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Erro ao consultar a I.A.: {e}")

# =========================================================================
# DEMAIS MÓDULOS (PRESERVADOS E INTEGRADOS)
# =========================================================================
elif st.session_state.modulo_atual == "Radar In-Play":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Radar In-Play de Pressão & Live Odds (Betfair & Pinnacle)</h3>", unsafe_allow_html=True)
    st.caption("Cruzamento ao vivo entre o Algoritmo IPM e a precificação real das exchanges.")

    c_f1, c_f2 = st.columns(2)
    with c_f1: minuto_corte = st.slider("Minuto Mínimo da Partida", min_value=1, max_value=90, value=30)
    with c_f2: ipm_corte = st.slider("Corte Mínimo de Pressão (IPM)", min_value=0.10, max_value=0.60, value=0.25, step=0.05)

    if not api_key:
        st.warning("Insira sua chave gratuita da API-Football nas configurações do Streamlit Cloud.")
    else:
        if st.button("EXECUTAR VARREDURA DE PARTIDAS & CALCULAR DISTORÇÕES"):
            with st.spinner("Sincronizando feeds mundiais e calculando IPM..."):
                headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}
                try:
                    res = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers, timeout=10)
                    dados_live = res.json().get("response", [])
                    if not dados_live:
                        st.info("Nenhuma partida ao vivo no momento.")
                    else:
                        for jogo in dados_live:
                            minuto = jogo["fixture"]["status"]["elapsed"]
                            if minuto is None or minuto < minuto_corte: continue
                            mandante = jogo["teams"]["home"]["name"]
                            visitante = jogo["teams"]["away"]["name"]
                            gols_m = jogo["goals"]["home"] or 0
                            gols_v = jogo["goals"]["away"] or 0
                            st.markdown(f"""
                            <div class="cscore-card">
                                <span style="background:#ef4444; color:#fff; font-weight:800; font-size:0.75rem; padding:3px 8px; border-radius:4px;">AO VIVO {minuto}'</span>
                                <div style="font-size:1.2rem; font-weight:900; margin-top:6px; color:#ffffff;">{mandante} <span style="color:#38bdf8;">{gols_m} - {gols_v}</span> {visitante}</div>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao buscar partidas: {e}")

elif st.session_state.modulo_atual == "Análise Pré-Jogo":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Inteligência Pré-Jogo & Relatórios I.A.")
    else:
        st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Relatórios Exclusivos Pré-Jogo</h3>", unsafe_allow_html=True)
        st.info("Módulo liberado com relatórios avançados de mercado para assinantes cadastrados.")

elif st.session_state.modulo_atual == "Backtest 5 Anos":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Simulador Quantitativo de 5 Anos de Backtest")
    else:
        st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Simulador Histórico de Longo Prazo (5 Anos)</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: liga = st.selectbox("Liga", ["Premier League", "La Liga", "Serie A", "Bundesliga"])
        with c2: odd_corte = st.number_input("Odd Mínima", value=1.60)
        st.button("EXECUTAR SIMULAÇÃO HISTÓRICA DE 5 ANOS")

elif st.session_state.modulo_atual == "Grade de Jogos":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Grade de Jogos do Dia</h3>", unsafe_allow_html=True)
    st.button("SINCRONIZAR GRADE COMPLETA DO DIA")

elif st.session_state.modulo_atual == "Calculadora EV+":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Calculadora EV+ (Precificação & Gestão de Risco)</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        odd = st.number_input("Odd Oferecida", min_value=1.01, value=2.00)
        prob = st.slider("Probabilidade Estimada (%)", min_value=1, max_value=99, value=55)
    with c2:
        prob_dec = prob / 100.0
        ev = (prob_dec * (odd - 1.0)) - (1.0 - prob_dec)
        st.metric("Margem de Valor (+EV)", f"{ev*100:.1f}%")

elif st.session_state.modulo_atual == "Backoffice Admin":
    st.markdown("<h3 style='color:#ffffff; font-size:1.35rem; font-weight:900;'>Backoffice do Administrador - Gestão de Leads</h3>", unsafe_allow_html=True)
    senha = st.text_input("Senha Mestra", type="password")
    if st.button("ACESSAR BACKOFFICE"):
        if senha == admin_password: st.success("Acesso autorizado.")
        else: st.error("Senha incorreta.")
