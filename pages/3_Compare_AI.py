import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ai.openai_client import call_openai_recommendations

# Carregar dados
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches.")

user_prompt = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Analyzing with AI and comparing players..."):
        # STEP 1 – Get ideal attributes from OpenAI
        try:
            # Prompt for ideal attributes in JSON
            attr_prompt = (
                "Based on the following description, return ideal values (0–100) for these attributes: "
                "Pace, Shooting, Passing, Dribbling, Defending, Physical, Vision, Composure, Ball_Control. "
                "Return only a JSON like: {\"Pace\": 90, \"Shooting\": 85, ...}"
            )
            ideal_json = call_openai_recommendations(f"{user_prompt}\n\n{attr_prompt}")

            ideal_attributes = eval(ideal_json)
            ideal_vector = np.array([ideal_attributes[attr] for attr in attribute_cols]).reshape(1, -1)

            # STEP 2 – Compute similarities
            player_vectors = players_df[attribute_cols].values
            similarities = cosine_similarity(ideal_vector, player_vectors)[0]
            players_df["Similarity"] = similarities

            top3 = players_df.sort_values("Similarity", ascending=False).head(3)

            # STEP 3 – Get AI recommendation text
            recommendation_report = call_openai_recommendations(user_prompt)

            # STEP 4 – Show
            st.markdown("## ✨ AI Recommendation Report")
            st.markdown(recommendation_report)

        except Exception as e:
            st.error(f"AI response error: {e}")
            st.code(ideal_json)
