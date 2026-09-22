import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & INJEÇÃO DE CSS PROFISSIONAL (DARK FINTECH)
# =========================================================================
st.set_page_config(
    page_title="AlphaBet | Quantitative Trading Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para dar acabamento de Terminal Institucional
st.markdown("""
<style>
    /* Estilo geral da aplicação */
    .stApp {
        background-color: #0b0e14;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Títulos e Tipografia */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* Container de cartões personalizados */
    .metric-card {
        background: #141923;
        border: 1px solid #232b3e;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .metric-card:hover {
        border-color: #3b82f6;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-positive {
        color: #10b981 !important;
    }
    .metric-negative {
        color: #ef4444 !important;
    }
    .metric-accent {
        color: #38bdf8 !important;
    }

    /* Abas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #232b3e;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0 20px;
        background-color: #141923;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
    }

    /* Botão Principal */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
        transform: translateY(-1px);
    }

    /* Botão de Download */
    div[data-testid="stDownloadButton"] > button {
        background: #0f172a;
        color: #38bdf8;
        border: 1px solid #0284c7;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 20px;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: #0284c7;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho Principal Estilo Terminal
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #232b3e; padding-bottom: 14px; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; display: flex; align-items: center; gap: 10px;">
            <span>⚡ ALPHABET</span> 
            <span style="font-size: 0.8rem; background: #1e293b; color: #38bdf8; padding: 4px 10px; border-radius: 20px; border: 1px solid #38bdf8;">PRO TERMINAL</span>
        </h1>
        <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">Modelagem Estatística, Precificação Justa e Backtest Quantitativo de 5 Anos</p>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.8rem; color: #10b981; font-weight: 600;">● SISTEMA OPERACIONAL ATIVO</span><br>
        <span style="font-size: 0.75rem; color: #64748b;">Dados: Football-Data.co.uk API Layer</span>
    </div>
</div>
""", unsafe_allow_html=True)

aba_backtest, aba_analise = st.tabs(["🧪 Backtest Quantitativo (5 Anos)", "🧮 Calculadora de Valor (+EV) & Kelly"])

# =========================================================================
# ABA 1: MOTOR DE BACKTEST MULTI-TEMPORADAS
# =========================================================================
with aba_backtest:
    # Barra de Configurações em Cards
    with st.container():
        st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-bottom:12px;'>⚙️ Parâmetros do Teste de Estresse</h4>", unsafe_allow_html=True)
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
    if st.button("🚀 Executar Simulação Quantitativa (5 Anos)"):
        barra_progresso = st.progress(0)
        status_texto = st.empty()

        lista_dataframes = []
        cod_liga = mapa_ligas[liga_escolhida]

        for i, temp in enumerate(temporadas):
            status_texto.markdown(f"<span style='color:#94a3b8; font-size:0.85rem;'>Sincronizando temporada {temp['nome']}...</span>", unsafe_allow_html=True)
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

        status_texto.empty()
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

                # =========================================================
                # CARDS MÉTRICOS MODERNOS (HTML/CSS)
                # =========================================================
                st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-top:20px;'>📊 Performance Executiva (5 Anos)</h4>", unsafe_allow_html=True)
                m1, m2, m3, m4, m5 = st.columns(5)

                lucro_classe = "metric-positive" if lucro_acumulado >= 0 else "metric-negative"
                lucro_sinal = "+" if lucro_acumulado >= 0 else ""

                with m1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Amostra Filtrada</div>
                        <div class="metric-value metric-accent">{total_jogos} <span style="font-size:0.9rem; color:#64748b;">jogos</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Taxa de Acerto (Win Rate)</div>
                        <div class="metric-value">{win_rate:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Lucro Líquido Acumulado</div>
                        <div class="metric-value {lucro_classe}">{lucro_sinal}R$ {lucro_acumulado:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Yield / ROI Global</div>
                        <div class="metric-value {lucro_classe}">{lucro_sinal}{roi:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m5:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Max Drawdown (Pior Queda)</div>
                        <div class="metric-value metric-negative">-R$ {drawdown_maximo:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")

                # =========================================================
                # GRÁFICOS NO ESTILO TERMINAL DE TRADING
                # =========================================================
                col_g1, col_g2 = st.columns([3, 2])

                with col_g1:
                    # Curva de Capital Suave com Área Sombreada
                    fig_curva = go.Figure()
                    fig_curva.add_trace(go.Scatter(
                        x=list(range(len(historico_banca))),
                        y=historico_banca,
                        mode='lines',
                        name='Saldo Líquido',
                        line=dict(color='#38bdf8', width=2.5),
                        fill='tozeroy',
                        fillcolor='rgba(56, 189, 248, 0.08)'
                    ))
                    fig_curva.update_layout(
                        title="<b>Curva de Patrimônio Líquido (Equity Curve)</b>",
                        paper_bgcolor='#0b0e14',
                        plot_bgcolor='#141923',
                        font=dict(color='#94a3b8'),
                        xaxis=dict(showgrid=True, gridcolor='#232b3e', title="Sequência de Entradas"),
                        yaxis=dict(showgrid=True, gridcolor='#232b3e', title="Saldo (R$)"),
                        margin=dict(l=20, r=20, t=40, b=20),
                        height=350
                    )
                    st.plotly_chart(fig_curva, use_container_width=True)

                with col_g2:
                    # Comparativo Anual em Barras Coloridas
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
                        title="<b>Resultado por Ano Fiscal</b>",
                        paper_bgcolor='#0b0e14',
                        plot_bgcolor='#141923',
                        font=dict(color='#94a3b8'),
                        xaxis=dict(gridcolor='#232b3e'),
                        yaxis=dict(gridcolor='#232b3e', title="Lucro (R$)"),
                        margin=dict(l=20, r=20, t=40, b=20),
                        height=350
                    )
                    st.plotly_chart(fig_barras, use_container_width=True)

                # =========================================================
                # TABELA E EXPORTAÇÃO PROFISSIONAL
                # =========================================================
                st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-top:16px;'>📄 Auditoria de Operações Individuais</h4>", unsafe_allow_html=True)
                
                csv_bytes = df_relatorio.drop(columns=['Acerto', 'Volume']).to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')

                col_down, col_space = st.columns([1, 3])
                with col_down:
                    st.download_button(
                        label="⬇️ Exportar Registro Completo (.CSV / Excel)",
                        data=csv_bytes,
                        file_name=f"audit_{cod_liga}_{mercado.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )

                st.dataframe(
                    df_relatorio.drop(columns=['Acerto', 'Volume']).tail(20),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("⚠️ Nenhuma partida atendeu à faixa de odds selecionada. Experimente expandir os critérios.")

# =========================================================================
# ABA 2: CALCULADORA DE VALOR (+EV) & CRITÉRIO DE KELLY
# =========================================================================
with aba_analise:
    st.markdown("<h4 style='color:#cbd5e1; font-size:1.1rem; margin-bottom:12px;'>Precificação Precisa & Dimensionamento de Posição</h4>", unsafe_allow_html=True)
    c_in1, c_in2 = st.columns(2)

    with c_in1:
        st.markdown("""
        <div class="metric-card" style="margin-bottom: 20px;">
            <div class="metric-label" style="color:#38bdf8;">1. Parâmetros de Cotação e Probabilidade</div>
        </div>
        """, unsafe_allow_html=True)
        odd_oferecida = st.number_input("Odd da Exchange / Bookmaker", min_value=1.01, max_value=50.0, value=2.00, step=0.05)
        probabilidade = st.slider("Probabilidade Estimada pelo Modelo (%)", min_value=1, max_value=99, value=55)
        banca_atual = st.number_input("Capital da Banca Disponível (R$)", min_value=10.0, value=1000.0, step=50.0)

    with c_in2:
        prob_decimal = probabilidade / 100.0
        odd_justa = 1.0 / prob_decimal
        ev = (prob_decimal * (odd_oferecida - 1.0)) - (1.0 - prob_decimal)

        st.markdown("""
        <div class="metric-card" style="margin-bottom: 20px;">
            <div class="metric-label" style="color:#38bdf8;">2. Veredito Matemático</div>
        </div>
        """, unsafe_allow_html=True)

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

            st.markdown(f"""
            <div style="background:#064e3b; border:1px solid #10b981; border-radius:8px; padding:16px; margin-top:10px;">
                <h4 style="margin:0; color:#10b981; font-size:1rem;">✅ ENTRADA COM VANTAGEM MATEMÁTICA</h4>
                <p style="margin:4px 0 0 0; color:#d1fae5; font-size:0.9rem;">
                    Stake Recomendada (1/4 Kelly Conservador): <b>R$ {stake_sugerida:.2f}</b> ({((stake_sugerida/banca_atual)*100):.2f}% da banca)
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#450a0a; border:1px solid #ef4444; border-radius:8px; padding:16px; margin-top:10px;">
                <h4 style="margin:0; color:#ef4444; font-size:1rem;">❌ ENTRADA SEM VALOR MATEMÁTICO</h4>
                <p style="margin:4px 0 0 0; color:#fee2e2; font-size:0.9rem;">
                    A odd oferecida é inferior à probabilidade do evento. Entrada com expectativa de perda a longo prazo.
                </p>
            </div>
            """, unsafe_allow_html=True)
