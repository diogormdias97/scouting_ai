import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai
import os

# --- Configuração da API ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Carregar os dados ---
games_df = pd.read_csv("data/games.csv")
players_df = pd.read_csv("data/players_data.csv")

# --- Corrigir nomes de colunas (se necessário) ---
games_df.columns = games_df.columns.str.strip()
players_df.columns = players_df.columns.str.strip()

# --- Interface ---
st.title("📊 Game-by-game Stats")

player_column_name = "Name" if "Name" in games_df.columns else games_df.columns[0]
player_names = games_df[player_column_name].unique()
selected_player = st.selectbox("Select a Player", player_names)

# --- Filtrar dados do jogador ---
player_data = games_df[games_df[player_column_name] == selected_player]

# --- Atributos esperados ---
attributes = [
    "Shooting", "Passing", "Dribbling", "Defending",
    "Physical", "Vision", "Composure", "Ball_Control"
]

# --- Verificar atributos existentes ---
valid_attributes = [attr for attr in attributes if attr in player_data.columns]

# Debug temporário (remover depois de validar)
# st.write("Colunas disponíveis:", player_data.columns.tolist())
# st.write("Atributos considerados:", valid_attributes)

# --- Radar chart com médias dos atributos ---
st.subheader("🧠 Player Attributes")
try:
    attribute_values = player_data[valid_attributes].mean().round(0).astype(int)

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

except Exception as e:
    st.error(f"Error loading attributes: {e}")

# --- Estatísticas por jogo ---
st.subheader("📈 Game Stats")
try:
    st.dataframe(player_data)

except Exception as e:
    st.error(f"Error showing player data: {e}")

# --- Relatório com IA ---
st.subheader("🧠 AI Report")
if st.button("Generate Report"):
    try:
        prompt = f"Generate a scouting report for player {selected_player} based on the following stats:\n\n{player_data.to_string(index=False)}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        summary = response.choices[0].message["content"]
        st.markdown(summary)

    except Exception as e:
        st.error(f"Error generating AI summary: {e}")
        

        


