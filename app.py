import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Radar do Apostador", page_icon="📈", layout="wide")

st.title("🎯 Central de Análise & Trade Esportivo")
st.write("Calculadora de Valor Esperado (+EV) e Gestão de Banca em Tempo Real")

# Criando colunas visuais
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Parâmetros da Entrada")
    odd_oferecida = st.number_input("Odd da Casa / Exchange", min_value=1.01, max_value=50.0, value=2.00, step=0.05)
    probabilidade = st.slider("Sua Probabilidade Estimada (%)", min_value=1, max_value=99, value=55)
    banca_atual = st.number_input("Tamanho da sua Banca (R$)", min_value=10.0, value=1000.0, step=50.0)

with col2:
    st.subheader("📊 Diagnóstico da Aposta")
    prob_decimal = probabilidade / 100.0
    odd_justa = 1.0 / prob_decimal
    ev = (prob_decimal * (odd_oferecida - 1.0)) - (1.0 - prob_decimal)
    
    st.metric(label="Odd Justa Calculada", value=f"{odd_justa:.2f}")

    if ev > 0:
        lucro_esperado_pct = ev * 100
        st.success(f"✅ **Aposta com Valor Positivo!** (+EV de {lucro_esperado_pct:.1f}%)")
        # Critério de Kelly Fracionário (recomendando stake conservadora de 1/4 Kelly)
        b = odd_oferecida - 1.0
        q = 1.0 - prob_decimal
        kelly_full = (b * prob_decimal - q) / b
        stake_sugerida = max(0.0, (kelly_full / 4.0) * banca_atual)
        st.info(f"💡 Sugestão de Stake (1/4 Kelly): **R$ {stake_sugerida:.2f}**")
    else:
        st.error("❌ **Aposta sem Valor matemático** (EV Negativo). Entrada desaconselhada a longo prazo.")
