import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
try:
    players_df = pd.read_csv("data/players_data.csv")
    games_df = pd.read_csv("data/games.csv")
except Exception as e:
    st.error(f"Erro ao carregar ficheiros CSV: {e}")
    st.stop()

# Verifica colunas obrigatórias
expected_players_cols = {"Name", "Age", "Club", "Position", "Goals", "Assists", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical", "Vision", "Composure", "Ball_Control"}
expected_games_cols = {"Name", "Match", "Goals", "Assists", "Minutes"}

missing_p_cols = expected_players_cols - set(players_df.columns)
missing_g_cols = expected_games_cols - set(games_df.columns)

if missing_p_cols:
    st.error(f"Colunas em falta no players_data.csv: {missing_p_cols}")
    st.stop()

if missing_g_cols:
    st.error(f"Colunas em falta no games.csv: {missing_g_cols}")
    st.stop()

# Interface
st.title("📊 Game-by-game Stats")
selected_player = st.selectbox("Select a Player", players_df["Name"].unique())
st.markdown("### ⚙️ Player Attributes")

# Extrair dados do jogador
player_data = players_df[players_df["Name"] == selected_player]
if player_data.empty:
    st.warning("Jogador não encontrado.")
    st.stop()

# Mostrar info
st.write("**Age:**", int(player_data["Age"].values[0]))
st.write("**Club:**", player_data["Club"].values[0])
st.write("**Position:**", player_data["Position"].values[0])

# Atributos
attributes = [
    "Goals", "Assists", "Pace", "Shooting", "Passing", "Dribbling",
    "Defending", "Physical", "Vision", "Composure", "Ball_Control"
]

attribute_values = player_data[attributes].values.flatten()

# Bar chart
fig, ax = plt.subplots()
ax.barh(attributes, attribute_values)
ax.set_title(f"Atributos de {selected_player}")
ax.invert_yaxis()
st.pyplot(fig)

# Dados de jogo
st.markdown("### 📅 Game Stats")
player_game_data = games_df[games_df["Name"] == selected_player]

if player_game_data.empty:
    st.info("Sem jogos para este jogador.")
else:
    st.dataframe(player_game_data)

    # Gráfico linha
    fig2, ax2 = plt.subplots()
    ax2.plot(player_game_data["Match"], player_game_data["Goals"], marker='o', label="Goals")
    ax2.plot(player_game_data["Match"], player_game_data["Assists"], marker='s', label="Assists")
    ax2.set_title(f"Desempenho por Jogo - {selected_player}")
    ax2.set_xlabel("Match")
    ax2.set_ylabel("Contagem")
    ax2.legend()
    st.pyplot(fig2)

        


