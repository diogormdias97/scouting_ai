import streamlit as st
import pandas as pd
from ai.openai_client import call_openai_recommendations

# --- Load data ---
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

user_prompt = st.text_area("🗣️ Describe your ideal player", "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        # Lista de nomes válidos
        player_names = players_df["Name"].dropna().unique().tolist()
        
        # Chamada à API OpenAI com recomendação
        ai_recommendation = call_openai_recommendations(user_prompt, player_names)

        if ai_recommendation.startswith("AI response error"):
            st.error(ai_recommendation)
        else:
            st.markdown("## ✨ AI Recommendation Report")
            st.markdown(ai_recommendation)
