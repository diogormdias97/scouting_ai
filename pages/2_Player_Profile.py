# pages/2_Player_Profile.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Configuração da página ----------
st.set_page_config(page_title="Player Profile", layout="wide")
st.title("📊 Player Profile")

# ---------- Carregar dados ----------
try:
    players_df = pd.read_csv("data/players_data.csv")
    games_df   = pd.read_csv("data/games.csv")
except FileNotFoundError:
    st.error("❌ Ficheiros CSV não encontrados em /data.")
    st.stop()

# Limpa espaços e normaliza maiúsculas/minúsculas
players_df.columns = players_df.columns.str.strip()
games_df.columns   = games_df.columns.str.strip()
players_df["Name_clean"] = players_df["Name"].str.strip().str.lower()
games_df["Name_clean"]   = games_df["Name"].str.strip().str.lower()

# ---------- Seleção do jogador ----------
player_names = players_df["Name"].dropna().sort_values().tolist()
selected_player = st.selectbox("Select a Player", player_names)
player_key      = selected_player.strip().lower()       # chave de comparação

# ---------- Secção de Atributos ----------
st.subheader("⚙️ Player Attributes")

if player_key not in players_df["Name_clean"].values:
    st.error(f"❌ Jogador '{selected_player}' não encontrado nos dados.")
    st.stop()

player_row  = players_df.loc[players_df["Name_clean"] == player_key].iloc[0]

fifa_attrs = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]
missing    = [a for a in fifa_attrs if a not in players_df.columns]

if missing:
    st.error(f"❌ Atributos em falta no CSV: {', '.join(missing)}")
else:
    values = [player_row[a] for a in fifa_attrs]
    fig = px.line_polar(
        r     = values + [values[0]],
        theta = fifa_attrs + [fifa_attrs[0]],
        line_close=True,
        title = f"{selected_player} – Skill Radar",
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Estatísticas jogo-a-jogo ----------
st.subheader("📈 Game-by-game Stats")

# Garantir colunas mínimas
req_cols = {"Name", "Match", "Goals", "Assists"}
if not req_cols.issubset(games_df.columns):
    st.error(f"❌ O ficheiro games.csv tem de conter as colunas: {', '.join(req_cols)}")
else:
    player_games = games_df.loc[games_df["Name_clean"] == player_key]

    if player_games.empty:
        st.info(f"ℹ️ Sem dados de jogos disponíveis para **{selected_player}**.")
    else:
        fig2 = px.line(
            player_games, x="Match", y=["Goals", "Assists"],
            markers=True, title=f"{selected_player} – G/A por jogo"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ---------- Atributos crus ----------
st.subheader("📋 Raw Attributes")
st.dataframe(player_row.drop("Name_clean").to_frame(), use_container_width=True)


