import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

# Carrega dados
players_df = pd.read_csv("data/players_data.csv")
players_df.set_index("Name", inplace=True)

# Substitui experimental
query_params = st.query_params
selected_player = query_params.get("name", [None])[0] if query_params else None

# Lista dropdown para navegação
dropdown = st.selectbox("Select a player", players_df.index.tolist(), index=players_df.index.get_loc(selected_player) if selected_player in players_df.index else 0)

# Se mudar no dropdown, atualiza o URL
if dropdown != selected_player:
    st.query_params["name"] = dropdown
    selected_player = dropdown

player_row = players_df.loc[selected_player]

# Título e dados
st.title("🧑‍🏫 Player Profile")
st.header(f"{selected_player}")
st.markdown(f"**Position:** {player_row['Position']} | **Foot:** {player_row['Foot']}")
st.markdown(f"**Age:** {player_row['Age']} | **Height:** {player_row['Height_cm']} cm | **Weight:** {player_row['Weight_kg']} kg")

# Gráfico de atributos
st.subheader("⚽ Attributes")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control', 'Avg_Rating']

fig = px.bar(
    x=attribute_cols,
    y=player_row[attribute_cols].values,
    labels={"x": "Attribute", "y": "Score"},
    title="Attribute Ratings",
    text=player_row[attribute_cols].values
)
fig.update_traces(marker_color='rgb(58, 124, 209)', textposition='outside')
fig.update_layout(yaxis=dict(range=[0, 100]))

st.plotly_chart(fig)


