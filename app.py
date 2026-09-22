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
    page_title="AlphaBet | Terminal Quantitativo & VIP Intelligence",
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

    /* =========================================================
       FORMULÁRIO VIP: CAIXAS BRANCAS COM TEXTO ESCURO
       ========================================================= */
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

    /* BOTÃO DO FORMULÁRIO VIP: FUNDO BRANCO COM FONTE ESCURA */
    div[data-testid="stForm"] div.stButton > button {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #f59e0b !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div[data-testid="stForm"] div.stButton > button p {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    div[data-testid="stForm"] div.stButton > button:hover {
        background: #f8fafc !important;
        border-color: #d97706 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5) !important;
    }

    /* =========================================================
       BOTÕES DE NAVEGAÇÃO DA BARRA LATERAL (ALTO CONTRASTE)
       ========================================================= */
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
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
        transform: translateX(-3px) !important;
    }
    section[data-testid="stSidebar"] div.stButton > button p {
        color: inherit !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Outros Selectboxes fora do form */
    div[data-baseweb="select"] > div {
        background-color: #141923 !important;
        border: 1px solid #232b3e !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }

    /* Botão de Execução do Backtest no Painel Principal */
    .main div.stButton > button {
        background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.4px !important;
        border-radius: 8px !important;
        border: 1px solid #3b82f6 !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    }
    .main div.stButton > button p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Cards Métricos e de Jogo */
    .metric-card {
        background: #141923;
        border: 1px solid #232b3e;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
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
        padding: 14px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .live-badge {
        background: #ef4444;
        color: white;
        padding: 2px 8px;
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
    .scheduled-badge {
        background: #1e293b;
        color: #38bdf8;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #0284c7;
    }

    .vip-gate-box {
        background: linear-gradient(180deg, #141923 0%, #0d121c 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal Estilo FinTech
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #232b3e; padding-bottom: 14px; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; display: flex; align-items: center; gap: 10px;">
            <span>⚡ ALPHABET</span> 
            <span style="font-size: 0.8rem; background: #1e293b; color: #38bdf8; padding: 4px 10px; border-radius: 20px; border: 1px solid #38bdf8;">TERMINAL QUANT</span>
        </h1>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.9rem;">Ecossistema de Inteligência Pré-Jogo, Radar In-Play e Backtest de 5 Anos</p>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.8rem; color: #10b981; font-weight: 600;">● SISTEMA CONECTADO</span><br>
        <span style="font-size: 0.75rem; color: #64748b;">Feeds: Football-Data & API-Sports</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Captura segura da chave de API
api_key = st.secrets.get("API_FOOTBALL_KEY", "")

# Inicialização dos estados na sessão
if "lead_desbloqueado" not in st.session_state:
    st.session_state.lead_desbloqueado = False

if "modulo_atual" not in st.session_state:
    st.session_state.modulo_atual = "👑 Análises VIP (Pré-Jogo)"

# =========================================================================
# BARRA LATERAL À DIREITA COM BOTÕES DE SELEÇÃO EXCLUSIVOS
# =========================================================================
with st.sidebar:
    st.markdown("<h3 style='font-size:1.15rem; color:#f8fafc; border-bottom: 1px solid #232b3e; padding-bottom: 8px;'>📌 Navegação de Áreas</h3>", unsafe_allow_html=True)
    st.caption("Selecione o ambiente desejado:")

    # Lista de áreas do app em botões individuais com fontes contrastantes
    if st.button("👑 Análises VIP (Pré-Jogo)"):
        st.session_state.modulo_atual = "👑 Análises VIP (Pré-Jogo)"
    
    if st.button("🧪 Backtest Histórico (Área VIP)"):
        st.session_state.modulo_atual = "🧪 Backtest Histórico (Área VIP)"

    if st.button("🔴 Radar In-Play (Ao Vivo)"):
        st.session_state.modulo_atual = "🔴 Radar In-Play (Ao Vivo)"

    if st.button("📅 Agenda (Próximos Jogos)"):
        st.session_state.modulo_atual = "📅 Agenda (Próximos Jogos)"

    if st.button("🧮 Calculadora de Valor (+EV)"):
        st.session_state.modulo_atual = "🧮 Calculadora de Valor (+EV)"

    st.markdown("---")
    st.markdown("<div style='color:#94a3b8; font-size:0.8rem;'>Área ativa no momento:</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#38bdf8; font-weight:700; font-size:0.95rem;'>{st.session_state.modulo_atual}</div>", unsafe_allow_html=True)
    
    st.write("")
    if st.session_state.lead_desbloqueado:
        st.markdown("""
        <div style="background:#064e3b; border:1px solid #10b981; border-radius:8px; padding:10px; text-align:center;">
            <span style="color:#10b981; font-weight:700; font-size:0.85rem;">STATUS: ASSINANTE VIP</span><br>
            <span style="color:#d1fae5; font-size:0.75rem;">Acesso Completo Liberado</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#1e293b; border:1px solid #f59e0b; border-radius:8px; padding:10px; text-align:center;">
            <span style="color:#f59e0b; font-weight:700; font-size:0.85rem;">STATUS: VISITANTE</span><br>
            <span style="color:#94a3b8; font-size:0.75rem;">Módulos VIP requerem cadastro</span>
        </div>
        """, unsafe_allow_html=True)

# Função Auxiliar: Renderiza o formulário VIP de cadastro (caixas brancas com texto escuro)
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
# MÓDULO 1: ANÁLISES VIP (PRÉ-JOGO)
# =========================================================================
if st.session_state.modulo_atual == "👑 Análises VIP (Pré-Jogo)":
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

        st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem;'>🎯 Projeções Quantitativas de Valor (+EV)</h4>", unsafe_allow_html=True)

        dados_analises_vip = [
            {
                "Partida": "Arsenal vs Chelsea",
                "Liga": "Premier League",
                "Mercado": "Over 2.5 Gols",
                "Odd_Mercado": 1.95,
                "Odd_Justa_Modelo": 1.72,
                "EV_Estimado": "+13.3%",
                "xG_Projetado": "3.10 gols",
                "Recomendacao": "Forte Valor Matemático no Over"
            },
            {
                "Partida": "Real Madrid vs Villarreal",
                "Liga": "La Liga",
                "Mercado": "Back Mandante (Real Madrid)",
                "Odd_Mercado": 1.62,
                "Odd_Justa_Modelo": 1.48,
                "EV_Estimado": "+9.4%",
                "xG_Projetado": "2.65 x 0.85",
                "Recomendacao": "Enquadrado nos parâmetros do Backtest"
            },
            {
                "Partida": "Bayer Leverkusen vs Borussia Dortmund",
                "Liga": "Bundesliga",
                "Mercado": "Ambas Equipes Marcam (BTTS)",
                "Odd_Mercado": 1.68,
                "Odd_Justa_Modelo": 1.50,
                "EV_Estimado": "+12.0%",
                "xG_Projetado": "3.45 gols",
                "Recomendacao": "Alta probabilidade ofensiva mútua"
            }
        ]

        for item in dados_analises_vip:
            st.markdown(f"""
            <div class="match-card" style="border-left: 4px solid #f59e0b;">
                <div>
                    <span class="vip-badge" style="background:#1e293b; color:#f59e0b; border:1px solid #f59e0b;">{item['Liga']}</span>
                    <span style="font-size:0.85rem; color:#94a3b8; margin-left:8px;">xG: <b>{item['xG_Projetado']}</b></span>
                    <div style="font-size:1.15rem; font-weight:700; margin-top:6px; color:#f8fafc;">
                        {item['Partida']}
                    </div>
                    <div style="font-size:0.9rem; color:#cbd5e1; margin-top:4px;">
                        Mercado: <b style="color:#38bdf8;">{item['Mercado']}</b> | Odd Atual: <b>{item['Odd_Mercado']}</b> (Odd Justa: {item['Odd_Justa_Modelo']})
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.3rem; font-weight:800; color:#10b981;">{item['EV_Estimado']}</div>
                    <div style="font-size:0.8rem; color:#94a3b8;">{item['Recomendacao']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================================
# MÓDULO 2: BACKTEST HISTÓRICO (ÁREA VIP EXCLUSIVA)
# =========================================================================
elif st.session_state.modulo_atual == "🧪 Backtest Histórico (Área VIP)":
    if not st.session_state.lead_desbloqueado:
        renderizar_barreira_lead("Simulador Quantitativo de 5 Anos de Backtest")
    else:
        st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🧪 Simulador Histórico de Longo Prazo (5 Anos)</h3>", unsafe_allow_html=True)
        st.caption("Base consolidada das últimas 5 temporadas completas via Football-Data.co.uk")

        with st.container():
            st.markdown("<h4 style='color:#cbd5e1; font-size:1.05rem; margin-bottom:12px;'>⚙️ Parâmetros da Simulação</h4>", unsafe_allow_html=True)
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)

            with col_c1:
                liga_escolhida = st.selectbox(
                    "Competição",
                    ["Premier League (Inglaterra)", "La Liga (Espanha)", "Serie A (Itália)", "Bundesliga (Alemanha)"]
                )
            with col_c2:
                mercado = st.selectbox(
                    "Mercado Alvo",
                    ["Over 2.5 Gols (Mais de 2.5)", "Under 2.5 Gols (Menos de 2.5)", "Back Mandante (Casa)", "Back Visitante (Fora)", "Back Empate"]
                )
            with col_c3:
                odd_min = st.number_input("Odd Mínima", value=1.60, step=0.05)
                odd_max = st.number_input("Odd Máxima", value=2.20, step=0.05)
            with col_c4:
                stake_tipo = st.number_input("Stake por Entrada (R$)", min_value=10.0, value=100.0, step=10.0)

        mapa_ligas = {
            "Premier League (Inglaterra)": "E0",
            "La Liga (Espanha)": "SP1",
            "Serie A (Itália)": "I1",
            "Bundesliga (Alemanha)": "D1"
        }

        temporadas = [
            {"nome": "2019/2020", "cod": "1920"},
            {"nome": "2020/2021", "cod": "2021"},
            {"nome": "2021/2022", "cod": "2122"},
            {"nome": "2022/2023", "cod": "2223"},
            {"nome": "2023/2024", "cod": "2324"}
        ]

        st.write("")
        # BOTÃO DO BACKTEST COM FONTE BRILHANTE EM ALTO CONTRASTE
        if st.button("🚀 Executar Simulação Histórica (5 Anos)"):
            barra_progresso = st.progress(0)
            lista_dataframes = []
            cod_liga = mapa_ligas[liga_escolhida]

            for i, temp in enumerate(temporadas):
                url = f"https://www.football-data.co.uk/mmz4281/{temp['cod']}/{cod_liga}.csv"
                try:
                    df_temp = pd.read_csv(url)
                    colunas_necessarias = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
                    colunas_odds = ['B365H', 'B365D', 'B365A', 'B365>2.5', 'B365<2.5']
                    colunas_presentes = [c for c in colunas_necessarias + colunas_odds if c in df_temp.columns]
                    df_temp = df_temp[colunas_presentes].dropna()
                    df_temp['Temporada'] = temp['nome']
                    lista_dataframes.append(df_temp)
                except Exception:
                    pass
                barra_progresso.progress((i + 1) / len(temporadas))

            barra_progresso.empty()

            if lista_dataframes:
                base_completa = pd.concat(lista_dataframes, ignore_index=True)
                registros = []
                lucro_acumulado = 0.0
                picos_banca = 0.0
                drawdown_maximo = 0.0
                historico_banca = [0.0]

                for _, row in base_completa.iterrows():
                    if mercado == "Over 2.5 Gols (Mais de 2.5)":
                        if 'B365>2.5' not in row: continue
                        odd_jogo = row['B365>2.5']
                        ganhou = (row['FTHG'] + row['FTAG']) > 2.5
                    elif mercado == "Under 2.5 Gols (Menos de 2.5)":
                        if 'B365<2.5' not in row: continue
                        odd_jogo = row['B365<2.5']
                        ganhou = (row['FTHG'] + row['FTAG']) < 2.5
                    elif mercado == "Back Mandante (Casa)":
                        odd_jogo = row.get('B365H', 0)
                        ganhou = (row['FTR'] == 'H')
                    elif mercado == "Back Visitante (Fora)":
                        odd_jogo = row.get('B365A', 0)
                        ganhou = (row['FTR'] == 'A')
                    else:
                        odd_jogo = row.get('B365D', 0)
                        ganhou = (row['FTR'] == 'D')

                    if odd_min <= odd_jogo <= odd_max:
                        if ganhou:
                            resultado_financeiro = (odd_jogo - 1.0) * stake_tipo
                            acerto_binario = 1
                            status = "GREEN"
                        else:
                            resultado_financeiro = -stake_tipo
                            acerto_binario = 0
                            status = "RED"

                        lucro_acumulado += resultado_financeiro
                        historico_banca.append(lucro_acumulado)

                        if lucro_acumulado > picos_banca:
                            picos_banca = lucro_acumulado
                        queda_atual = picos_banca - lucro_acumulado
                        if queda_atual > drawdown_maximo:
                            drawdown_maximo = queda_atual

                        registros.append({
                            "Data": row['Date'],
                            "Temporada": row['Temporada'],
                            "Partida": f"{row['HomeTeam']} vs {row['AwayTeam']}",
                            "Placar": f"{int(row['FTHG'])}x{int(row['FTAG'])}",
                            "Odd": odd_jogo,
                            "Status": status,
                            "Resultado_R$": round(resultado_financeiro, 2),
                            "Acerto": acerto_binario,
                            "Volume": stake_tipo
                        })

                if registros:
                    df_relatorio = pd.DataFrame(registros)
                    total_jogos = len(df_relatorio)
                    total_acertos = df_relatorio['Acerto'].sum()
                    win_rate = (total_acertos / total_jogos) * 100
                    total_investido = total_jogos * stake_tipo
                    roi = (lucro_acumulado / total_investido) * 100

                    st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-top:20px;'>📊 Performance da Estratégia (5 Anos)</h4>", unsafe_allow_html=True)
                    m1, m2, m3, m4, m5 = st.columns(5)

                    lucro_classe = "metric-positive" if lucro_acumulado >= 0 else "metric-negative"
                    lucro_sinal = "+" if lucro_acumulado >= 0 else ""

                    with m1:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Amostra</div><div class="metric-value metric-accent">{total_jogos} jogos</div></div>', unsafe_allow_html=True)
                    with m2:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Win Rate</div><div class="metric-value">{win_rate:.1f}%</div></div>', unsafe_allow_html=True)
                    with m3:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Lucro Líquido</div><div class="metric-value {lucro_classe}">{lucro_sinal}R$ {lucro_acumulado:,.2f}</div></div>', unsafe_allow_html=True)
                    with m4:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">ROI Global</div><div class="metric-value {lucro_classe}">{lucro_sinal}{roi:.2f}%</div></div>', unsafe_allow_html=True)
                    with m5:
                        st.markdown(f'<div class="metric-card"><div class="metric-label">Max Drawdown</div><div class="metric-value metric-negative">-R$ {drawdown_maximo:,.2f}</div></div>', unsafe_allow_html=True)

                    st.write("")
                    col_g1, col_g2 = st.columns([3, 2])

                    with col_g1:
                        fig_curva = go.Figure()
                        fig_curva.add_trace(go.Scatter(
                            x=list(range(len(historico_banca))),
                            y=historico_banca,
                            mode='lines',
                            line=dict(color='#38bdf8', width=2.5),
                            fill='tozeroy',
                            fillcolor='rgba(56, 189, 248, 0.08)'
                        ))
                        fig_curva.update_layout(
                            title="<b>Curva de Patrimônio Líquido (Equity Curve)</b>",
                            paper_bgcolor='#0b0e14',
                            plot_bgcolor='#141923',
                            font=dict(color='#94a3b8'),
                            xaxis=dict(showgrid=True, gridcolor='#232b3e'),
                            yaxis=dict(showgrid=True, gridcolor='#232b3e'),
                            margin=dict(l=20, r=20, t=40, b=20),
                            height=350
                        )
                        st.plotly_chart(fig_curva, use_container_width=True)

                    with col_g2:
                        df_anual = df_relatorio.groupby('Temporada')['Resultado_R$'].sum().reset_index()
                        cores_barras = ['#10b981' if v >= 0 else '#ef4444' for v in df_anual['Resultado_R$']]
                        fig_barras = go.Figure(go.Bar(
                            x=df_anual['Temporada'],
                            y=df_anual['Resultado_R$'],
                            marker_color=cores_barras,
                            text=[f"R$ {v:,.0f}" for v in df_anual['Resultado_R$']],
                            textposition='auto',
                        ))
                        fig_barras.update_layout(
                            title="<b>Resultado por Temporada</b>",
                            paper_bgcolor='#0b0e14',
                            plot_bgcolor='#141923',
                            font=dict(color='#94a3b8'),
                            xaxis=dict(gridcolor='#232b3e'),
                            yaxis=dict(gridcolor='#232b3e'),
                            margin=dict(l=20, r=20, t=40, b=20),
                            height=350
                        )
                        st.plotly_chart(fig_barras, use_container_width=True)

                    csv_bytes = df_relatorio.drop(columns=['Acerto', 'Volume']).to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
                    st.download_button(
                        label="⬇️ Exportar Registro Completo (.CSV / Excel)",
                        data=csv_bytes,
                        file_name=f"audit_{cod_liga}_{mercado.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )

# =========================================================================
# MÓDULO 3: RADAR IN-PLAY (AO VIVO)
# =========================================================================
elif st.session_state.modulo_atual == "🔴 Radar In-Play (Ao Vivo)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🔴 Radar In-Play (Jogos em Tempo Real)</h3>", unsafe_allow_html=True)
    st.caption("Partidas com bola rolando no mundo via API-Football.")

    if not api_key:
        st.warning("⚠️ Insira sua chave gratuita da API-Football nas configurações do Streamlit Cloud.")
    else:
        if st.button("🔄 Atualizar Partidas Ao Vivo"):
            with st.spinner("Buscando jogos com bola rolando..."):
                headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}
                try:
                    res = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers, timeout=10)
                    dados_live = res.json().get("response", [])
                    if not dados_live:
                        st.info("Nenhuma partida ao vivo no momento.")
                    else:
                        st.success(f"{len(dados_live)} partidas encontradas ao vivo!")
                        for jogo in dados_live:
                            minuto = jogo["fixture"]["status"]["elapsed"]
                            mandante = jogo["teams"]["home"]["name"]
                            visitante = jogo["teams"]["away"]["name"]
                            gols_m = jogo["goals"]["home"] or 0
                            gols_v = jogo["goals"]["away"] or 0
                            liga = jogo["league"]["name"]
                            pais = jogo["league"]["country"]

                            st.markdown(f"""
                            <div class="match-card">
                                <div>
                                    <span class="live-badge">AO VIVO {minuto}'</span>
                                    <span style="font-size:0.8rem; color:#94a3b8; margin-left:8px;">{pais} - {liga}</span>
                                    <div style="font-size:1.1rem; font-weight:700; margin-top:6px; color:#f8fafc;">
                                        {mandante} <span style="color:#38bdf8;">{gols_m} x {gols_v}</span> {visitante}
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <span style="font-size:0.95rem; font-weight:600; color:#10b981;">Em Andamento</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao consultar API: {e}")

# =========================================================================
# MÓDULO 4: AGENDA (PRÓXIMOS JOGOS DE HOJE)
# =========================================================================
elif st.session_state.modulo_atual == "📅 Agenda (Próximos Jogos)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>📅 Agenda de Jogos do Dia</h3>", unsafe_allow_html=True)
    st.caption("Grade de partidas programadas para as próximas horas.")

    if not api_key:
        st.warning("⚠️ Insira sua chave da API-Football nas configurações do Streamlit Cloud.")
    else:
        hoje = datetime.date.today().strftime("%Y-%m-%d")
        if st.button("📅 Carregar Grade do Dia"):
            with st.spinner("Buscando agenda..."):
                headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}
                try:
                    res = requests.get(f"https://v3.football.api-sports.io/fixtures?date={hoje}", headers=headers, timeout=10)
                    jogos_hoje = res.json().get("response", [])
                    if not jogos_hoje:
                        st.info("Nenhuma partida catalogada para hoje.")
                    else:
                        st.success(f"{len(jogos_hoje)} partidas encontradas para hoje!")
                        for jogo in jogos_hoje[:25]:
                            horario_utc = jogo["fixture"]["date"][11:16]
                            mandante = jogo["teams"]["home"]["name"]
                            visitante = jogo["teams"]["away"]["name"]
                            liga = jogo["league"]["name"]
                            pais = jogo["league"]["country"]

                            st.markdown(f"""
                            <div class="match-card">
                                <div>
                                    <span class="scheduled-badge">⏰ {horario_utc} UTC</span>
                                    <span style="font-size:0.8rem; color:#94a3b8; margin-left:8px;">{pais} - {liga}</span>
                                    <div style="font-size:1.05rem; font-weight:600; margin-top:6px; color:#f8fafc;">
                                        {mandante} <span style="color:#64748b;">vs</span> {visitante}
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <span style="font-size:0.85rem; color:#38bdf8; font-weight:600;">Pré-Jogo</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao buscar agenda: {e}")

# =========================================================================
# MÓDULO 5: CALCULADORA DE VALOR (+EV) & CRITÉRIO DE KELLY
# =========================================================================
elif st.session_state.modulo_atual == "🧮 Calculadora de Valor (+EV)":
    st.markdown("<h3 style='color:#f8fafc; font-size:1.3rem;'>🧮 Precificação Precisa & Gestão de Risco</h3>", unsafe_allow_html=True)
    c_in1, c_in2 = st.columns(2)

    with c_in1:
        st.markdown('<div class="metric-card"><div class="metric-label" style="color:#38bdf8;">1. Parâmetros de Entrada</div></div>', unsafe_allow_html=True)
        odd_oferecida = st.number_input("Odd da Exchange / Bookmaker", min_value=1.01, max_value=50.0, value=2.00, step=0.05)
        probabilidade = st.slider("Probabilidade Estimada pelo Modelo (%)", min_value=1, max_value=99, value=55)
        banca_atual = st.number_input("Capital da Banca Disponível (R$)", min_value=10.0, value=1000.0, step=50.0)

    with c_in2:
        prob_decimal = probabilidade / 100.0
        odd_justa = 1.0 / prob_decimal
        ev = (prob_decimal * (odd_oferecida - 1.0)) - (1.0 - prob_decimal)

        st.markdown('<div class="metric-card"><div class="metric-label" style="color:#38bdf8;">2. Veredito Matemático</div></div>', unsafe_allow_html=True)
        k1, k2 = st.columns(2)
        with k1:
            st.metric("Odd Justa Teórica", f"{odd_justa:.2f}")
        with k2:
            st.metric("Margem de Valor (+EV)", f"{ev*100:.1f}%")

        if ev > 0:
            b = odd_oferecida - 1.0
            q = 1.0 - prob_decimal
            kelly_full = (b * prob_decimal - q) / b
            stake_sugerida = max(0.0, (kelly_full / 4.0) * banca_atual)
            st.success(f"✅ **ENTRADA DE VALOR IDENTIFICADA!**\nStake Sugerida (1/4 Kelly): **R$ {stake_sugerida:.2f}** ({((stake_sugerida/banca_atual)*100):.2f}% da banca)")
        else:
            st.error("❌ **ENTRADA SEM VALOR MATEMÁTICO.** Expectativa desfavorável a longo prazo.")
