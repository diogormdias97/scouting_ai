import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt
import openai
import os

# --- Configuração da API ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Carregar os dados ---
games_df = pd.read_csv("data/games.csv")
players_df = pd.read_csv("data/players_data.csv")

# Corrigir espaços nos nomes das colunas
games_df.columns = games_df.columns.str.strip()
players_df.columns = players_df.columns.str.strip()

# --- Interface ---
st.title("📊 Game-by-game Stats")

# Selecionar jogador com base nos nomes do ficheiro de jogos
player_column_name = "Name" if "Name" in games_df.columns else games_df.columns[0]
player_names = games_df[player_column_name].unique()
selected_player = st.selectbox("Select a Player", player_names)

# --- Filtrar dados por jogo ---
player_game_data = games_df[games_df[player_column_name] == selected_player]

# --- Game Stats ---
st.subheader("📈 Game Stats")
if player_game_data.empty:
    st.warning("No game data found for this player.")
else:
    st.dataframe(player_game_data)

# --- Atributos individuais do jogador (players_data.csv) ---
st.subheader("⚙️ Player Attributes")

# Procurar no players_df os atributos do jogador
player_profile = players_df[players_df["Name"] == selected_player]

# Lista de atributos esperados
attributes = [
    "Shooting", "Passing", "Dribbling", "Defending",
    "Physical", "Vision", "Composure", "Ball_Control"
]

# Verifica se o jogador existe no ficheiro de atributos
if not player_profile.empty:
    valid_attributes = [attr for attr in attributes if attr in player_profile.columns]
    attribute_values = player_profile[valid_attributes].iloc[0].astype(int)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = [n / float(len(valid_attributes)) * 2 * 3.14159 for n in range(len(valid_attributes))]
    values = attribute_values.tolist()
    values += values[:1]
    angles += angles[:1]

    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, alpha=0.4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(valid_attributes)
    ax.set_title(f"Attributes Radar: {selected_player}")
    st.pyplot(fig)
else:
    st.warning("Player not found in attributes file.")

# --- Relatório com IA ---
st.subheader("🧠 AI Report")
if st.button("Generate Report"):
    try:
        prompt = f"Generate a scouting report for player {selected_player} based on the following stats:\n\n{player_game_data.to_string(index=False)}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        summary = response.choices[0].message["content"]
        st.markdown(summary)

    except Exception as e:
        st.error(f"Error generating AI summary: {e}")

        


