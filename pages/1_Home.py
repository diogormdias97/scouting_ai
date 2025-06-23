# Página principal de pesquisa de jogadores
import streamlit as st
import pandas as pd
from utils.data_loader import load_data

st.set_page_config(page_title="Player Search", layout="wide")

st.title("🔍 Player Search")

# Load player data
df = load_data()

# Sidebar filters
st.sidebar.header("Filter players")

name_filter = st.sidebar.text_input("Name")
club_filter = st.sidebar.text_input("Club")
position_filter = st.sidebar.selectbox("Position", ["", "GK", "DEF", "MID", "FWD"])

# Advanced filters
st.sidebar.subheader("Advanced Filters")
min_goals = st.sidebar.number_input("Minimum Goals", min_value=0, value=0)
max_age = st.sidebar.number_input("Maximum Age", min_value=0, value=99)

# Apply filters
filtered_df = df.copy()

if name_filter:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(name_filter, case=False)]

if club_filter:
    filtered_df = filtered_df[filtered_df["Club"].str.contains(club_filter, case=False)]

if position_filter:
    filtered_df = filtered_df[filtered_df["Position"] == position_filter]

filtered_df = filtered_df[filtered_df["Goals"] >= min_goals]
filtered_df = filtered_df[filtered_df["Age"] <= max_age]

# Display results
st.markdown("### Results")
if filtered_df.empty:
    st.warning("No players found with these filters.")
else:
    st.dataframe(filtered_df[["Name", "Age", "Club", "Position", "Goals", "Assists"]].sort_values(by="Goals", ascending=False), use_container_width=True)
    st.info("Click a player in the list to view the full profile (coming soon).")
