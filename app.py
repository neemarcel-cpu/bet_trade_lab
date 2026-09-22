import streamlit as st
import pandas as pd
import plotly.express as px

# ================= CONFIGURAÇÃO VISUAL =================
st.set_page_config(page_title="Central Quantitativa de Apostas", page_icon="📊", layout="wide")

st.title("🎯 Central do Apostador: Análise & Backtest")

# Criando sistema de abas para organizar as ferramentas
aba_analise, aba_backtest = st.tabs(["🧮 Calculadora de Valor (+EV)", "🧪 Simulador de Backtest"])

# =========================================================================
# ABA 1: CALCULADORA DE VALOR (+EV) & CRITÉRIO DE KELLY
# =========================================================================
with aba_analise:
    st.subheader("Calculadora de Valor Esperado (+EV) & Gestão de Risco")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ⚙️ Parâmetros da Aposta")
        odd_oferecida = st.number_input("Odd da Casa / Exchange", min_value=1.01, max_value=50.0, value=2.00, step=0.05)
        probabilidade = st.slider("Sua Probabilidade Estimada (%)", min_value=1, max_value=99, value=55)
        banca_atual = st.number_input("Tamanho da Banca (R$)", min_value=10.0, value=1000.0, step=50.0)

    with col2:
        st.markdown("### 📊 Resultado Matemático")
        prob_decimal = probabilidade / 100.0
        odd_justa = 1.0 / prob_decimal
        ev = (prob_decimal * (odd_oferecida - 1.0)) - (1.0 - prob_decimal)
        
        st.metric("Odd Justa Mínima", f"{odd_justa:.2f}")

        if ev > 0:
            lucro_esperado = ev * 100
            st.success(f"✅ **Entrada de Valor Encontrada!** (+EV de {lucro_esperado:.1f}%)")
            b = odd_oferecida - 1.0
            q = 1.0 - prob_decimal
            kelly_full = (b * prob_decimal - q) / b
            stake_fracionaria = max(0.0, (kelly_full / 4.0) * banca_atual)
            st.info(f"💡 Stake recomendada (1/4 Kelly): **R$ {stake_fracionaria:.2f}**")
        else:
            st.error("❌ **Aposta sem valor matemático** (EV negativo). Não recomendada a longo prazo.")

# =========================================================================
# ABA 2: MOTOR DE BACKTEST HISTÓRICO
# =========================================================================
with aba_backtest:
    st.subheader("Simulador Histórico de Estratégias")
    st.caption("Dados oficiais históricos de fechamento obtidos via Football-Data.co.uk")

    # 1. Painel de Controle de Parâmetros
    c1, c2, c3 = st.columns(3)
    with c1:
        liga_escolhida = st.selectbox(
            "Selecione a Liga",
            options=["Premier League (Inglaterra)", "La Liga (Espanha)", "Serie A (Itália)", "Bundesliga (Alemanha)"]
        )
    with c2:
        temporada = st.selectbox(
            "Temporada",
            options=["2023/2024", "2022/2023", "2021/2022"]
        )
    with c3:
        stake_tipo = st.number_input("Valor da Stake Fixa (R$)", min_value=10.0, value=100.0, step=10.0)

    # Mapeamento dos códigos da fonte de dados
    mapa_ligas = {
        "Premier League (Inglaterra)": "E0",
        "La Liga (Espanha)": "SP1",
        "Serie A (Itália)": "I1",
        "Bundesliga (Alemanha)": "D1"
    }
    mapa_temp = {
        "2023/2024": "2324",
        "2022/2023": "2223",
        "2021/2022": "2122"
    }

    # Filtros da Estratégia
    st.markdown("#### 🎯 Regras da Estratégia a Testar")
    f1, f2, f3 = st.columns(3)
    with f1:
        mercado = st.selectbox("Mercado de Entrada", ["Back Mandante (Casa)", "Back Visitante (Fora)", "Back Empate"])
    with f2:
        odd_min = st.number_input("Odd Mínima de Entrada", value=1.50, step=0.05)
    with f3:
        odd_max = st.number_input("Odd Máxima de Entrada", value=2.20, step=0.05)

    # Botão para Executar a Simulação
    if st.button("🚀 Rodar Backtest Agora"):
        with st.spinner("Baixando base de dados históricos e processando resultados..."):
            cod_liga = mapa_ligas[liga_escolhida]
            cod_temp = mapa_temp[temporada]
            url = f"https://www.football-data.co.uk/mmz4281/{cod_temp}/{cod_liga}.csv"

            try:
                df = pd.read_csv(url)
                # Garantir que as colunas necessárias existam
                colunas_necessarias = ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A']
                df = df[colunas_necessarias].dropna()

                # Mapeamento do resultado esperado e coluna da odd
                if mercado == "Back Mandante (Casa)":
                    col_odd = 'B365H'
                    res_alvo = 'H'
                elif mercado == "Back Visitante (Fora)":
                    col_odd = 'B365A'
                    res_alvo = 'A'
                else:
                    col_odd = 'B365D'
                    res_alvo = 'D'

                lucro_acumulado = 0.0
                total_entradas = 0
                acertos = 0
                total_apostado = 0.0
                historico_banca = [0.0]

                # Loop pelas partidas da temporada
                for _, row in df.iterrows():
                    odd_jogo = row[col_odd]
                    resultado_real = row['FTR']

                    # Aplica o filtro de odd definido
                    if odd_min <= odd_jogo <= odd_max:
                        total_entradas += 1
                        total_apostado += stake_tipo

                        if resultado_real == res_alvo:
                            lucro_rodada = (odd_jogo - 1.0) * stake_tipo
                            acertos += 1
                        else:
                            lucro_rodada = -stake_tipo

                        lucro_acumulado += lucro_rodada
                        historico_banca.append(lucro_acumulado)

                # Exibir Métricas se houver entradas
                if total_entradas > 0:
                    win_rate = (acertos / total_entradas) * 100
                    roi = (lucro_acumulado / total_apostado) * 100

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Entradas Realizadas", f"{total_entradas} jogos")
                    m2.metric("Taxa de Acerto", f"{win_rate:.1f}%")
                    m3.metric("Lucro Líquido", f"R$ {lucro_acumulado:.2f}", delta=f"{lucro_acumulado:.2f}")
                    m4.metric("ROI / Yield", f"{roi:.2f}%")

                    # Gráfico Interativo com Plotly
                    df_grafico = pd.DataFrame({
                        "Número da Aposta": list(range(len(historico_banca))),
                        "Lucro Acumulado (R$)": historico_banca
                    })

                    fig = px.line(
                        df_grafico, 
                        x="Número da Aposta", 
                        y="Lucro Acumulado (R$)",
                        title="Curva de Capital da Estratégia",
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("Nenhum jogo nesta temporada atendeu à faixa de odds selecionada. Experimente alargar os filtros.")

            except Exception as erro:
                st.error(f"Erro ao consultar dados históricos: {erro}")
