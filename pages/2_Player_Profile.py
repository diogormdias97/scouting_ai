import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse

# Carrega os dados
players_df = pd.read_csv("data/players_data.csv")
games_df = pd.read_csv("data/games.csv")

# Página de perfil
st.title("🧑‍💼 Player Profile")

# Verifica se há nome na URL
query_params = st.experimental_get_query_params()
default_name = query_params["name"][0] if "name" in query_params else players_df.iloc[0]["Name"]

# Caixa de seleção de jogador
selected_name = st.selectbox("Select a player", sorted(players_df["Name"].unique()), index=0)
if selected_name != default_name:
    st.experimental_set_query_params(name=urllib.parse.quote(selected_name))
else:
    selected_name = urllib.parse.unquote(default_name)

# Filtra o jogador
player_row = players_df.set_index("Name").loc[selected_name]

st.header(selected_name)

st.markdown(f"""
**Position:** {player_row['Position']} | **Foot:** {player_row['Foot']}  
**Age:** {player_row['Age']} | **Height:** {player_row['Height_cm']} cm | **Weight:** {player_row['Weight_kg']} kg
""")

# Atributos
st.subheader("⚽ Attributes")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control', 'Avg_Rating']

attribute_scores = player_row[attribute_cols]

fig, ax = plt.subplots()
ax.bar(attribute_scores.index, attribute_scores.values)
plt.xticks(rotation=45)
plt.ylabel("Score")
st.pyplot(fig)

# Estatísticas da época
st.subheader("📊 Season Summary")

player_games = games_df[games_df["Name"] == selected_name]
if not player_games.empty:
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

    st.write(season_stats.to_frame().T)

    st.markdown("### Match History")
    st.dataframe(player_games[["Match", "Minutes", "Rating", "Goals", "Assists", "Yellow_Cards", "Red_Cards"]].reset_index(drop=True))
else:
    st.warning("No game data found for this player.")

