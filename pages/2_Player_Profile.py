import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utils.data_loader import load_data
from ai.openai_client import generate_summary

st.set_page_config(page_title="Player Profile", layout="wide")

st.title("📋 Player Profile")

# Load data
df = load_data()

# Select player
player_names = df["Name"].unique().tolist()
selected_player = st.selectbox("Select a player", player_names)

# Get player data
player_data = df[df["Name"] == selected_player].iloc[0]

# FIFA-style attributes (0–20 scale)
fifa_attributes = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]
fifa_values = [player_data[attr] for attr in fifa_attributes]

# Radar chart
st.subheader("🛡️ Attributes (FIFA-style)")
fig = px.line_polar(
    r=fifa_values + [fifa_values[0]],
    theta=fifa_attributes + [fifa_attributes[0]],
    line_close=True,
    title=f"{selected_player} - Skill Radar",
)
st.plotly_chart(fig, use_container_width=True)

# Game-by-game stats
st.subheader("📊 Game-by-game Stats")
games_df = pd.read_csv("data/games.csv")  # assumes this exists
player_games = games_df[games_df["Name"] == selected_player]

fig2 = px.line(player_games, x="Match", y=["Goals", "Assists"], title="Goals & Assists per Match")
st.plotly_chart(fig2, use_container_width=True)

# Raw attributes
st.subheader("📌 Raw Attributes")
st.dataframe(player_data.to_frame(), use_container_width=True)

# AI Summary
st.subheader("🧠 AI Report")
if st.button("Generate Report"):
    summary = generate_summary(player_data.to_frame().T)
    st.markdown(summary)
