import streamlit as st
from utils.data_loader import load_players, load_games
import pandas as pd

st.set_page_config(page_title="Scouting AI - Home", layout="wide")
st.title("🔎 Player Search")

players_df = load_players()
games_df = load_games()

# --- Search bar ---
search_name = st.text_input("Search by player name")

# --- Advanced Filters ---
st.sidebar.header("Advanced Filters")
selected_clubs = st.sidebar.multiselect("Club", sorted(players_df["Club"].unique()))
age_range = st.sidebar.slider("Age Range", min_value=int(players_df["Age"].min()), max_value=int(players_df["Age"].max()), value=(9, 17))
height_range = st.sidebar.slider("Height (cm)", min_value=100, max_value=200, value=(140, 190))
selected_positions = st.sidebar.multiselect("Positions", sorted(players_df["Position"].unique()))
rating_min, rating_max = st.sidebar.slider("Avg Attribute Rating (0-100)", 0, 100, (50, 100))
goals_min = st.sidebar.number_input("Min Goals Last Season", 0, 50, 0)
assists_min = st.sidebar.number_input("Min Assists Last Season", 0, 50, 0)

# --- Calcular estatísticas agregadas ---
agg_stats = games_df.groupby("Name")[["Goals", "Assists"]].sum().rename(columns={
    "Goals": "GoalsLast",
    "Assists": "AssistsLast"
})
players_df = players_df.set_index("Name").join(agg_stats).fillna(0).reset_index()
players_df["AvgAttribute"] = players_df[[c for c in players_df.columns if players_df[c].dtype != "O" and c not in ["Age", "Height_cm", "Weight_kg", "GoalsLast", "AssistsLast"]]].mean(axis=1)

# --- Aplicar filtros ---
filtered = players_df.copy()
if search_name:
    filtered = filtered[filtered["Name"].str.contains(search_name, case=False)]
if selected_clubs:
    filtered = filtered[filtered["Club"].isin(selected_clubs)]
filtered = filtered[
    (filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1]) &
    (filtered["Height_cm"] >= height_range[0]) & (filtered["Height_cm"] <= height_range[1]) &
    (filtered["AvgAttribute"] >= rating_min) & (filtered["AvgAttribute"] <= rating_max) &
    (filtered["GoalsLast"] >= goals_min) &
    (filtered["AssistsLast"] >= assists_min)
]
if selected_positions:
    filtered = filtered[filtered["Position"].isin(selected_positions)]

# --- Tabela de resultados ---
st.markdown("### 🎯 Matching Players")
selected_player = st.selectbox("Select a player", filtered["Name"]) if not search_name else search_name
st.dataframe(filtered[["Name", "Age", "Club", "Position", "AvgAttribute", "GoalsLast", "AssistsLast"]])

# Guardar seleção para a página seguinte
if st.button("Go to Profile"):
    st.session_state.selected_player = selected_player
    st.switch_page("pages/2_Player_Profile.py")
