import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.graph_objects as go

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & CSS DARK FINTECH PROFISSIONAL
# =========================================================================
st.set_page_config(
    page_title="AlphaBet | Quant & In-Play Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    /* Estilo dos Cards Métricos */
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

    /* Card de Jogo Ao Vivo / Próximo */
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
        animation: blinker 1.5s linear infinite;
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
    @keyframes blinker {
        50% { opacity: 0.3; }
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #232b3e; padding-bottom: 14px; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; display: flex; align-items: center; gap: 10px;">
            <span>⚡ ALPHABET</span> 
            <span style="font-size: 0.8rem; background: #1e293b; color: #38bdf8; padding: 4px 10px; border-radius: 20px; border: 1px solid #38bdf8;">TERMINAL INTEGRADO</span>
        </h1>
        <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">Backtest Quantitativo, Scanner In-Play e Agenda de Partidas</p>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.8rem; color: #10b981; font-weight: 600;">● SISTEMA CONECTADO</span><br>
        <span style="font-size: 0.75rem; color: #64748b;">Feeds: Football-Data & API-Sports</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Captura segura da chave de API
api_key = st.secrets.get("API_FOOTBALL_KEY", "")

# 4 Abas completas do ecossistema
aba_live, aba_proximos, aba_backtest, aba_calc = st.tabs([
    "🔴 Radar In-Play (Ao Vivo)", 
    "📅 Agenda (Próximos Jogos)", 
    "🧪 Backtest Multi-Temporadas", 
    "🧮 Calculadora de Valor (+EV)"
])

# =========================================================================
# ABA 1: RADAR DE JOGOS AO VIVO (IN-PLAY)
# =========================================================================
with aba_live:
    st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem;'>Monitoramento em Tempo Real de Partidas</h4>", unsafe_allow_html=True)
    st.caption("Identifique jogos no 2º tempo com placar parelho para entradas dinâmicas em Back/Lay.")

    if not api_key:
        st.warning("⚠️ Chave da API-Football não configurada nos Secrets do Streamlit Cloud.")
        st.info("Insira sua chave gratuita nas configurações do Streamlit Cloud sob o nome **API_FOOTBALL_KEY**.")
    else:
        col_btn, _ = st.columns([1, 4])
        with col_btn:
            atualizar_live = st.button("🔄 Atualizar Jogos Ao Vivo")

        if atualizar_live:
            with st.spinner("Conectando aos servidores globais e buscando jogos com bola rolando..."):
                headers = {
                    "x-rapidapi-host": "v3.football.api-sports.io",
                    "x-rapidapi-key": api_key
                }
                try:
                    url = "https://v3.football.api-sports.io/fixtures?live=all"
                    res = requests.get(url, headers=headers, timeout=10)
                    dados_live = res.json().get("response", [])

                    if not dados_live:
                        st.info("Nenhuma partida ao vivo no momento ou cota diária atingida.")
                    else:
                        st.success(f"{len(dados_live)} partidas encontradas ao vivo no mundo agora!")
                        
                        for jogo in dados_live:
                            minuto = jogo["fixture"]["status"]["elapsed"]
                            mandante = jogo["teams"]["home"]["name"]
                            visitante = jogo["teams"]["away"]["name"]
                            gols_m = jogo["goals"]["home"] if jogo["goals"]["home"] is not None else 0
                            gols_v = jogo["goals"]["away"] if jogo["goals"]["away"] is not None else 0
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
                                    <span style="font-size:0.85rem; color:#94a3b8;">Status da Rodada</span><br>
                                    <span style="font-size:0.95rem; font-weight:600; color:#10b981;">Em Andamento</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Erro ao consultar a API de jogos ao vivo: {e}")

# =========================================================================
# ABA 2: AGENDA (PRÓXIMOS JOGOS DE HOJE)
# =========================================================================
with aba_proximos:
    st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem;'>Agenda de Confrontos do Dia</h4>", unsafe_allow_html=True)
    st.caption("Filtre as partidas programadas para as próximas horas para planejar análises pré-jogo.")

    if not api_key:
        st.warning("⚠️ Insira sua API_FOOTBALL_KEY para carregar os confrontos do dia.")
    else:
        hoje = datetime.date.today().strftime("%Y-%m-%d")
        
        if st.button("📅 Carregar Grade de Jogos de Hoje"):
            with st.spinner("Buscando agenda de partidas para hoje..."):
                headers = {
                    "x-rapidapi-host": "v3.football.api-sports.io",
                    "x-rapidapi-key": api_key
                }
                try:
                    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
                    res = requests.get(url, headers=headers, timeout=10)
                    jogos_hoje = res.json().get("response", [])

                    if not jogos_hoje:
                        st.info("Nenhuma partida agendada encontrada para a data de hoje.")
                    else:
                        st.success(f"{len(jogos_hoje)} partidas catalogadas para o dia de hoje!")
                        
                        # Exibe os primeiros 25 jogos para não sobrecarregar
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
                    st.error(f"Erro ao buscar os próximos jogos: {e}")

# =========================================================================
# ABA 3: BACKTEST MULTI-TEMPORADAS (5 ANOS)
# =========================================================================
with aba_backtest:
    with st.container():
        st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-bottom:12px;'>⚙️ Parâmetros do Teste de Estresse Histórico</h4>", unsafe_allow_html=True)
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

                st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-top:20px;'>📊 Performance Executiva (5 Anos)</h4>", unsafe_allow_html=True)
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
# ABA 4: CALCULADORA DE VALOR (+EV) & KELLY
# =========================================================================
with aba_calc:
    st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-bottom:12px;'>Precificação Precisa & Dimensionamento de Posição</h4>", unsafe_allow_html=True)
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
            st.error("❌ **ENTRADA SEM VALOR MATEMÁTICO.** Expectativa matemática desfavorável a longo prazo.")
