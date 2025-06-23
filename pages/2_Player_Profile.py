import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from ai.openai_client import generate_summary

# Título da página
st.title("📊 Player Profile")

# Carrega os dados dos jogadores
df = load_data()

# Seleção de jogador
player_name = st.selectbox("Select a player", df["Name"].unique())
player_data = df[df["Name"] == player_name].iloc[0]

# Mostra os dados principais
st.subheader("📌 Basic Information")
st.write(f"**Club:** {player_data['Club']}")
st.write(f"**Age:** {player_data['Age']}")
st.write(f"**Position:** {player_data['Position']}")

# Atributos técnicos
st.subheader("🎯 Technical Attributes")
attributes = [
    "Goals", "Assists", "Pace", "Shooting", "Passing", "Dribbling",
    "Defending", "Physical", "Vision", "Composure", "Ball_Control"
]
st.dataframe(player_data[attributes].to_frame(), use_container_width=True)

# Estatísticas jogo a jogo
st.subheader("📈 Game-by-game Stats")
try:
    games_df = pd.read_csv("data/games.csv")  # Certifica-te que este ficheiro existe na pasta certa
    games_df = games_df[games_df["Name"] == player_name]

    fig = px.line(games_df, x="Match", y="Rating", title="Match Ratings Over Time")
    st.plotly_chart(fig, use_container_width=True)
except FileNotFoundError:
    st.warning("Game-by-game stats not available for this player.")

# Relatório gerado por IA
st.subheader("🧠 AI Report")
if st.button("Generate Report"):
    with st.spinner("Generating summary..."):
        try:
            summary = generate_summary(player_data[attributes].to_dict())
            st.success("Report generated:")
            st.write(summary)
        except Exception as e:
            st.error(f"Error generating AI summary: {e}")


