mport streamlit as st
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
            # Chamada ao modelo com os jogadores
            recommendation_text = call_openai_recommendations(description, players_df)

            st.markdown("## ✨ AI Recommendation Report")

            # Trata linha a linha a resposta
            for i, line in enumerate(recommendation_text.split("\n")):
                if not line.strip():
                    continue

                name = line.split(" - ")[0].strip()
                encoded_name = urllib.parse.quote(name)
                profile_url = f"/Player_Profile?name={encoded_name}"

                full_line = f"{line} [🔎 View Profile]({profile_url})"
                st.markdown(full_line)

        except Exception as e:
            st.error(f"AI response error: {e}")


