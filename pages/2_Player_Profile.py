import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Player Profile", layout="wide")

st.title("📊 Game-by-game Stats")

# === Carregar dados ===
try:
    players_df = pd.read_csv("data/players_data.csv")
    games_df = pd.read_csv("data/games.csv")
except FileNotFoundError:
    st.error("Erro: Ficheiros CSV não encontrados.")
    st.stop()

# Verifica e limpa espaços em branco nos nomes das colunas
players_df.columns = players_df.columns.str.strip()
games_df.columns = games_df.columns.str.strip()

# === Seleção do jogador ===
player_names = players_df["Name"].dropna().unique().tolist()
selected_player = st.selectbox("Select a Player", sorted(player_names))

# === Secção de Atributos ===
st.subheader("⚙️ Player Attributes")

# Verifica se o jogador está presente
if selected_player not in players_df["Name"].values:
    st.error(f"Jogador {selected_player} não encontrado.")
    st.stop()

# Extrair dados do jogador
player_data = players_df[players_df["Name"] == selected_player].iloc[0]

# Atributos tipo FIFA
fifa_attributes = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]
missing = [attr for attr in fifa_attributes if attr not in players_df.columns]
if missing:
    st.error(f"Atributos em falta no CSV: {', '.join(missing)}")
else:
    fifa_values = [player_data[attr] for attr in fifa_attributes]
    fig = px.line_polar(
        r=fifa_values + [fifa_values[0]],
        theta=fifa_attributes + [fifa_attributes[0]],
        line_close=True,
        title=f"{selected_player} - Skill Radar",
    )
    st.plotly_chart(fig, use_container_width=True)

# === Estatísticas jogo a jogo ===
st.subheader("📈 Game-by-game Stats")

if "Name" not in games_df.columns or "Match" not in games_df.columns:
    st.error("O ficheiro games.csv deve conter as colunas 'Name' e 'Match'.")
else:
    player_games = games_df[games_df["Name"] == selected_player]
    if not player_games.empty:
        fig2 = px.line(player_games, x="Match", y=["Goals", "Assists"], title="Goals & Assists per Match")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info(f"Sem dados de jogos disponíveis para {selected_player}.")

# === Atributos Crus ===
st.subheader("📋 Raw Attributes")
st.dataframe(player_data.to_frame(), use_container_width=True)

