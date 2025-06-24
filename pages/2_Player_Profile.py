import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import urllib.parse

# Dados
players_df = pd.read_csv("data/players_data.csv")
games_df = pd.read_csv("data/games.csv")

# Atributos e estatísticas
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control', 'Avg_Rating']
stat_cols = ['Avg_Rating', 'Goals_Last_Season', 'Assists_Last_Season', 'Yellow_Cards', 'Red_Cards']

# 📌 Obter o nome via parâmetro da URL ou dropdown
params = st.query_params
selected_name = params.get("name")

if selected_name is None:
    selected_name = st.selectbox("Select a player", players_df["Name"].tolist())
else:
    selected_name = urllib.parse.unquote(selected_name)
    st.selectbox("Select a player", players_df["Name"].tolist(), index=players_df[players_df["Name"] == selected_name].index[0])

# Filtrar jogador
player_row = players_df[players_df["Name"] == selected_name].iloc[0]

# Título e info
st.markdown("## 🧍 Player Profile")
st.markdown(f"### {player_row['Name']}")
st.markdown(f"**Position:** {player_row['Position']} | **Foot:** {player_row['Foot']}")
st.markdown(f"**Age:** {player_row['Age']} | **Height:** {player_row['Height_cm']} cm | **Weight:** {player_row['Weight_kg']} kg")

# Gráfico de atributos
st.markdown("### ⚽ Attributes")
fig = px.bar(x=attribute_cols, y=[player_row[col] for col in attribute_cols],
             labels={'x': 'Attribute', 'y': 'Score'},
             title="Attribute Ratings")
st.plotly_chart(fig, use_container_width=True)

# Estatísticas da época anterior
st.markdown("### 📊 General Statistics")
stats = {col: player_row[col] for col in stat_cols}
stats_df = pd.DataFrame(stats.items(), columns=["Statistic", "Value"])
st.table(stats_df)

# Resumo da época com base nos jogos
st.markdown("### 📅 Season Summary")
player_games = games_df[games_df["Name"] == selected_name]

if not player_games.empty:
    season_stats = player_games.agg({
        "Rating": "mean",
        "Minutes": "sum",
        "Goals": "sum",
        "Assists": "sum",
        "Yellow_Cards": "sum",
        "Red_Cards": "sum"
    }).rename({
        "Rating": "Avg Rating",
        "Minutes": "Total Minutes",
        "Goals": "Total Goals",
        "Assists": "Total Assists",
        "Yellow_Cards": "Total Yellow Cards",
        "Red_Cards": "Total Red Cards"
    })

    st.dataframe(season_stats.to_frame("Value"))
else:
    st.warning("No games registered for this player.")


