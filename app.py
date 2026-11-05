import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Projeção de Fluxo de Caixa", layout="wide")

# --- CUSTOM CSS (Estilização corrigida para usar unsafe_allow_html=True) ---
st.markdown("""
    <style>
    /* Estilo do fundo e containers */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Estilização dos cards de KPI */
    .kpi-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    .kpi-box.deficit {
        border-left: 5px solid #FF5252;
    }
    .kpi-title {
        font-size: 14px;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: bold;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #212529;
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.title("📊 Projeção de Fluxo de Caixa")
st.subheader("Antecipe a liquidez e tome decisões estratégicas")

# --- SIDEBAR: Entradas de Dados ---
st.sidebar.header("⚙️ Parâmetros Financeiros")
saldo_inicial = st.sidebar.number_input("Saldo Inicial em Caixa (R$)", value=10000.0, step=1000.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Previsão de Entradas (Receitas)")
receitas_m1 = st.sidebar.number_input("Mês 1 - Entradas", value=15000.0)
receitas_m2 = st.sidebar.number_input("Mês 2 - Entradas", value=18000.0)
receitas_m3 = st.sidebar.number_input("Mês 3 - Entradas", value=12000.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Previsão de Saídas (Despesas)")
despesas_m1 = st.sidebar.number_input("Mês 1 - Saídas", value=12000.0)
despesas_m2 = st.sidebar.number_input("Mês 2 - Saídas", value=13000.0)
despesas_m3 = st.sidebar.number_input("Mês 3 - Saídas", value=14000.0)

# --- PROCESSAMENTO DOS DADOS ---
s_m1 = saldo_inicial + receitas_m1 - despesas_m1
s_m2 = s_m1 + receitas_m2 - despesas_m2
s_m3 = s_m2 + receitas_m3 - despesas_m3

dados = {
    "Período": ["Mês 1", "Mês 2", "Mês 3"],
    "Entradas (R$)": [receitas_m1, receitas_m2, receitas_m3],
    "Saídas (R$)": [despesas_m1, despesas_m2, despesas_m3],
    "Saldo Final (R$)": [s_m1, s_m2, s_m3]
}
df = pd.DataFrame(dados)

# --- VISUALIZAÇÃO ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="kpi-box"><div class="kpi-title">Saldo Mês 1</div><div class="kpi-value">R$ {s_m1:,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-box"><div class="kpi-title">Saldo Mês 2</div><div class="kpi-value">R$ {s_m2:,.2f}</div></div>', unsafe_allow_html=True)
with col3:
    classe_deficit = "deficit" if s_m3 < 0 else ""
    st.markdown(f'<div class="kpi-box {classe_deficit}"><div class="kpi-title">Saldo Mês 3</div><div class="kpi-value">R$ {s_m3:,.2f}</div></div>', unsafe_allow_html=True)

col_grafico, col_tabela = st.columns(2)

with col_grafico:
    st.markdown("### 📈 Tendência do Saldo Acumulado")
    fig = px.line(df, x="Período", y="Saldo Final (R$)", markers=True, text="Saldo Final (R$)")
    fig.update_traces(textposition="top center", line_color="#4CAF50" if s_m3 >= 0 else "#FF5252")
    st.plotly_chart(fig, use_container_width=True)

with col_tabela:
    st.markdown("### 📋 Demonstrativo")
    st.dataframe(df.style.format({
        "Entradas (R$)": "R$ {:.2f}",
        "Saídas (R$)": "R$ {:.2f}",
        "Saldo Final (R$)": "R$ {:.2f}"
    }), hide_index=True, use_container_width=True)

if s_m3 < 0:
    st.error("⚠️ **Atenção:** A projeção indica que a empresa ficará sem liquidez no Mês 3.")
else:
    st.success("✅ **Saúde Financeira:** Projeção com liquidez positiva para os próximos 3 meses.")
