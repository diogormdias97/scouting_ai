import streamlit as st
import pandas as pd
import numpy as np
from ai.openai_client import call_openai_recommendations

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

            st.markdown("## ✨ AI Recommendation Report")
            st.markdown(recommendation_text)
        except Exception as e:
            st.error(f"AI response error: {e}")
