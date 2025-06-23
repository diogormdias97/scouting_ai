import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
players_df = pd.read_csv("data/players_data.csv")
games_df = pd.read_csv("data/games.csv")

# Garantir que as colunas têm os nomes corretos (case sensitive)
if "Name" not in players_df.columns or "Name" not in games_df.columns:
    st.error("Coluna 'Name' não encontrada. Verifica o nome exato no CSV.")
    st.stop()

# Sidebar: seleção de jogador
selected_player = st.selectbox("Select a Player", players_df["Name"].unique())

# Separador principal
st.title("📊 Game-by-game Stats")

# Player Attributes
st.markdown("### ⚙️ Player Attributes")

# Filtrar jogador
player_row = players_df[players_df["Name"] == selected_player]

if player_row.empty:
    st.warning("Jogador não encontrado nos dados.")
else:
    st.write("**Age:**", int(player_row["Age"].values[0]))
    st.write("**Club:**", player_row["Club"].values[0])
    st.write("**Position:**", player_row["Position"].values[0])

    # Mostrar atributos técnicos (excluindo colunas não numéricas)
    attribute_cols = [
        "Goals", "Assists", "Pace", "Shooting", "Passing", "Dribbling",
        "Defending", "Physical", "Vision", "Composure", "Ball_Control"
    ]
    attributes = player_row[attribute_cols].values.flatten()

    fig, ax = plt.subplots()
    ax.barh(attribute_cols, attributes)
    ax.invert_yaxis()
    ax.set_xlabel("Attribute Score")
    ax.set_title(f"Attributes for {selected_player}")
    st.pyplot(fig)

# Player Game Stats
st.markdown("### 📅 Game Stats")

# Filtrar jogos por jogador
player_games = games_df[games_df["Name"] == selected_player]

if player_games.empty:
    st.info("Sem dados de jogo para este jogador.")
else:
    st.dataframe(player_games)

    # Gráfico de golos por jogo
    fig, ax = plt.subplots()
    ax.plot(player_games["Match"], player_games["Goals"], marker='o', label="Goals")
    ax.plot(player_games["Match"], player_games["Assists"], marker='s', label="Assists")
    ax.set_title(f"Performance por Jogo - {selected_player}")
    ax.set_xlabel("Match")
    ax.set_ylabel("Count")
    ax.legend()
    st.pyplot(fig)

        


