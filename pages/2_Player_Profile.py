import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from ai.openai_client import generate_summary

st.set_page_config(page_title="Player Profile", layout="wide")
st.title("📊 Game-by-game Stats")

# Load main player data
df = load_data()

# Carregar dados dos jogos diretamente (sem função utilitária)
games_df = pd.read_csv("data/games.csv")

# Verifica nomes corretos
if "Name" not in df.columns or "Name" not in games_df.columns:
    st.error("Erro: A coluna 'Name' está em falta num dos ficheiros CSV.")
    st.stop()

# Seleção do jogador
player_names = df["Name"].unique().tolist()
selected_player = st.selectbox("Select a Player", player_names)

# Subconjunto dos dados do jogador
player_data = df[df["Name"] == selected_player]
if player_data.empty:
    st.warning("Jogador não encontrado nos dados.")
    st.stop()

player_row = player_data.iloc[0]

# --- ATRIBUTOS FIFA (RADAR CHART) ---
st.subheader("🧬 Player Attributes")

fifa_attributes = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]

# Verificação de atributos existentes
missing_attrs = [attr for attr in fifa_attributes if attr not in df.columns]
if missing_attrs:
    st.error(f"Atributos em falta: {missing_attrs}")
    st.stop()

fifa_values = [player_row[attr] for attr in fifa_attributes]

fig = px.line_polar(
    r=fifa_values + [fifa_values[0]],
    theta=fifa_attributes + [fifa_attributes[0]],
    line_close=True,
    title=f"{selected_player} - Skill Radar"
)
st.plotly_chart(fig, use_container_width=True)

# --- ESTATÍSTICAS JOGO A JOGO ---
st.subheader("📅 Game-by-game Performance")

player_games = games_df[games_df["Name"] == selected_player]

if not player_games.empty:
    fig2 = px.line(
        player_games,
        x="Match",
        y=["Goals", "Assists"],
        title="Goals & Assists per Match"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Este jogador ainda não tem estatísticas de jogo.")

# --- ATRIBUTOS BRUTOS ---
st.subheader("📋 Full Player Data")
st.dataframe(player_row.to_frame(), use_container_width=True)

# --- RELATÓRIO POR IA ---
st.subheader("🤖 AI Report")
if st.button("Generate Report"):
    with st.spinner("A gerar resumo com IA..."):
        report = generate_summary(player_row.to_frame().T)
        st.markdown(report)

