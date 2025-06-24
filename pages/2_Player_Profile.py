import streamlit as st
import pandas as pd
from utils.data_loader import load_players, load_games
import plotly.express as px

st.set_page_config(page_title="Player Profile", layout="wide")

players_df = load_players()
games_df = load_games()

# Obter jogador da sessão
if "selected_player" not in st.session_state:
    st.error("No player selected. Go back to Home page.")
    st.stop()

player_name = st.session_state.selected_player
player = players_df[players_df["Name"] == player_name].iloc[0]
player_games = games_df[games_df["Name"] == player_name]

# Dados principais
st.title(f"👤 {player['Name']}")
st.markdown(f"""
**Position:** {player['Position']} | **Foot:** {player['Foot']}  
**Age:** {player['Age']} | **Height:** {player['Height_cm']} cm | **Weight:** {player['Weight_kg']} kg
""")

# Atributos
attribute_cols = [col for col in players_df.columns if col not in ['Name', 'Age', 'Club', 'Position', 'Foot', 'Height_cm', 'Weight_kg', 'GoalsLast', 'AssistsLast', 'AvgAttribute']]
avg_rating = player[attribute_cols].mean()
st.subheader(f"⭐ Average Attribute Rating: {avg_rating:.1f}/100")

fig = px.bar(x=attribute_cols, y=[player[col] for col in attribute_cols], labels={"x": "Attribute", "y": "Score"})
st.plotly_chart(fig, use_container_width=True)

# Estatísticas da temporada
st.subheader("📊 Season Summary")
season_stats = player_games.agg({
    "AvgRating": "mean",
    "Goals": "sum",
    "Assists": "sum",
    "YellowCards": "sum",
    "RedCards": "sum"
})

st.markdown(f"""
- **Average Rating:** {season_stats['AvgRating']:.2f}
- **Goals:** {int(season_stats['Goals'])}
- **Assists:** {int(season_stats['Assists'])}
- **Yellow Cards:** {int(season_stats['YellowCards'])}
- **Red Cards:** {int(season_stats['RedCards'])}
""")

# Tabela de jogos
st.subheader("📅 Game-by-Game Performance")
st.dataframe(player_games, use_container_width=True)

# Gráfico de rating por jogo
fig2 = px.line(player_games, x="MatchID", y="AvgRating", title="Rating per Game")
st.plotly_chart(fig2, use_container_width=True)
