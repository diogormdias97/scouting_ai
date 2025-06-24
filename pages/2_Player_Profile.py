import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Player Profile", layout="wide")

st.title("👤 Player Profile")

# === Carregamento de dados ===
players_df = pd.read_csv("data/players_data.csv")
games_df = pd.read_csv("data/games.csv")

# === Seleção de jogador ===
player_names = players_df["Name"].dropna().unique().tolist()
selected_player = st.selectbox("Select a player", sorted(player_names))

# === Obter dados do jogador ===
player_data = players_df[players_df["Name"] == selected_player].iloc[0]
player_games = games_df[games_df["Name"] == selected_player]

# === Cabeçalho ===
st.markdown(f"## {selected_player}")
st.markdown(
    f"**Position:** {player_data['Position']} | "
    f"**Foot:** {player_data['Foot']}  \n"
    f"**Age:** {player_data['Age']} | "
    f"**Height:** {player_data['Height_cm']} cm | "
    f"**Weight:** {player_data['Weight_kg']} kg"
)

# === Secção de Atributos ===
st.markdown("### ⚽ Attributes")
attributes = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical",
              "Vision", "Composure", "Ball_Control"]
attr_df = pd.DataFrame({
    "Attribute": attributes + ["Avg_Rating"],
    "Score": [player_data[a] for a in attributes] + [player_data["Avg_Rating"]]
})
fig = px.bar(attr_df, x="Attribute", y="Score", title="Attribute Ratings", range_y=[0, 100])
st.plotly_chart(fig, use_container_width=True)

# === Estatísticas gerais ===
st.markdown("### 📊 General Stats")
stats = {
    "Avg Rating": player_data["Avg_Rating"],
    "Goals (Last Season)": player_data["Goals_Last_Season"],
    "Assists (Last Season)": player_data["Assists_Last_Season"],
    "Yellow Cards": player_data["Yellow_Cards"],
    "Red Cards": player_data["Red_Cards"]
}
for stat, val in stats.items():
    st.markdown(f"- **{stat}:** {val}")

# === Resumo da época ===
st.markdown("### 📈 Season Summary")
if player_games.empty:
    st.warning("No match data available for this player.")
else:
    try:
        season_stats = player_games.agg({
            "Rating": "mean",
            "Goals": "sum",
            "Assists": "sum",
            "Yellow_Cards": "sum",
            "Red_Cards": "sum"
        }).rename({
            "Rating": "Avg Rating",
            "Goals": "Goals",
            "Assists": "Assists",
            "Yellow_Cards": "Yellow Cards",
            "Red_Cards": "Red Cards"
        })
        st.dataframe(season_stats.to_frame().T, use_container_width=True)

        # === Gráfico de desempenho por jogo ===
        st.markdown("#### 📅 Game-by-Game Performance")
        fig2 = px.line(player_games, x="Match", y="Rating", title="Game Ratings")
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar resumo da época: {e}")
