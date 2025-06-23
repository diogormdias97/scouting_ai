# Página de recomendação IA por descrição
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from math import pi
from ai.openai_client import call_openai

# --- Carregar dados ---
players_df = pd.read_csv("data/players_100_youth_final.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

st.title("🎯 AI Player Finder")

st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest match!")

# --- Input do utilizador ---
user_prompt = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast winger with good dribbling and finishing, under 16 years old.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking the AI and comparing players..."):
        # --- Chamada à OpenAI ---
        system_msg = (
            "You are a football scout assistant. Based on the user's prompt, "
            "return the ideal values (0-20 scale) for the following attributes: "
            "Pace, Shooting, Passing, Dribbling, Defending, Physical, Vision, Composure, Ball_Control. "
            "Only return a JSON object like this: "
            '{"Pace": 18, "Shooting": 15, ..., "Ball_Control": 17}'
        )

        ideal_json = call_openai(user_prompt, system_msg)

        try:
            ideal_attributes = eval(ideal_json)  # simplificado para protótipo
            ideal_vector = np.array([ideal_attributes[attr] for attr in attribute_cols]).reshape(1, -1)

            # --- Calcular similaridade ---
            player_vectors = players_df[attribute_cols].values
            similarities = cosine_similarity(ideal_vector, player_vectors)[0]
            best_idx = np.argmax(similarities)
            best_player = players_df.iloc[best_idx]

            st.success(f"🏅 Best match: **{best_player['Name']}** ({best_player['Club']}, {best_player['Age']} yrs)")
            st.write("### Attributes Comparison")

            # --- Radar chart ---
            def plot_radar(player_vals, ideal_vals, labels):
                N = len(labels)
                angles = [n / float(N) * 2 * pi for n in range(N)]
                angles += angles[:1]
                player_vals += player_vals[:1]
                ideal_vals += ideal_vals[:1]

                fig, ax = plt.su
