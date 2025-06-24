import streamlit as st
import pandas as pd
from ai.openai_client import call_openai_recommendations

# --- Carrega os dados dos jogadores ---
players_df = pd.read_csv("data/players_data.csv")

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

user_prompt = st.text_area("🗣️ Describe your ideal player",
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        player_names = players_df["Name"].dropna().unique().tolist()
        ai_output = call_openai_recommendations(user_prompt, player_names)

    st.markdown("## ✨ AI Recommendation Report")
    st.markdown(ai_output)


