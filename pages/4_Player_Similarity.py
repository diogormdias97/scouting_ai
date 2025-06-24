import streamlit as st
import pandas as pd
import openai
from ai.openai_client import call_openai_similarity

players_df = pd.read_csv("data/players_data.csv")
selected_name = st.selectbox("Select a player", sorted(players_df["Name"].unique()))

if selected_name:
    player_row = players_df[players_df["Name"] == selected_name].iloc[0]
    with st.spinner("Asking AI for similar players..."):
        recommendation = call_openai_similarity(player_row, players_df)
    st.markdown("## 🧠 Similar Players (AI)")
    st.markdown(recommendation)
