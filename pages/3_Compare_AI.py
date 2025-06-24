import streamlit as st
import pandas as pd
import numpy as np
from ai.openai_client import call_openai_recommendations
import urllib.parse

# Load player data
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

description = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        try:
            # Filter candidates only (optional logic, e.g., age < 20)
            recommendation_text = call_openai_recommendations(description, players_df)

            sst.markdown("## ✨ AI Recommendation Report")

# Divide o texto da IA em linhas e trata cada recomendação
for i, line in enumerate(recommendation_text.split("\n")):
    if not line.strip():
        continue

    # Extrai o nome do jogador (antes do primeiro " - ")
    name = line.split(" - ")[0].strip()
    encoded_name = urllib.parse.quote(name)
    profile_url = f"/Player_Profile?name={encoded_name}"

    # Adiciona o link à linha
    full_line = f"{line} [🔎 View Profile]({profile_url})"
    st.markdown(full_line)
        except Exception as e:
            st.error(f"AI response error: {e}")
