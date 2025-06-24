import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load players
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ["Pace", "Shooting", "Passing", "Dribbling", "Defending",
                  "Physical", "Vision", "Composure", "Ball_Control"]

# Página
st.title("⚔️ Player Duel")

p1 = st.selectbox("Player 1", players_df["Name"])
p2 = st.selectbox("Player 2", players_df["Name"])

data1 = players_df[players_df["Name"] == p1][attribute_cols].values.flatten()
data2 = players_df[players_df["Name"] == p2][attribute_cols].values.flatten()

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=data1, theta=attribute_cols, fill='toself', name=p1))
fig.add_trace(go.Scatterpolar(r=data2, theta=attribute_cols, fill='toself', name=p2))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=True)

st.plotly_chart(fig, use_container_width=True)
