import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from openai import OpenAI
import json

# API Key (usa secrets se for no Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "sk-...")

# Carregar base de dados
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

# Interface
st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest match!")

# Input
user_prompt = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI and analyzing player attributes..."):

        # --- Chamada à OpenAI ---
        system_msg = (
            "You are a football scouting assistant. Based on the user's prompt, "
            "return the ideal attribute profile (scale 0-100) for the following attributes only: "
            "Pace, Shooting, Passing, Dribbling, Defending, Physical, Vision, Composure, Ball_Control. "
            "Only return a JSON object, like:\n"
            '{"Pace": 90, "Shooting": 75, "Passing": 80, "Dribbling": 88, "Defending": 40, '
            '"Physical": 78, "Vision": 74, "Composure": 79, "Ball_Control": 85}'
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )

            ideal_json = response.choices[0].message.content.strip()
            ideal_attributes = json.loads(ideal_json)

            # Verificar se todas as chaves esperadas estão presentes
            if not all(attr in ideal_attributes for attr in attribute_cols):
                st.error("⚠️ AI response missing some expected attributes.")
                st.json(ideal_json)
                st.stop()

            # Vetores para comparação
            ideal_vector = np.array([ideal_attributes[attr] for attr in attribute_cols]).reshape(1, -1)
            player_vectors = players_df[attribute_cols].values
            similarities = np.dot(player_vectors, ideal_vector.T).flatten()
            best_idx = np.argmax(similarities)
            best_player = players_df.iloc[best_idx]

            # Resultado
            st.success(f"🏅 Best Match: **{best_player['Name']}** ({best_player['Club']}, {best_player['Age']} yrs, {best_player['Position']})")

            # --- Radar Chart ---
            def plot_radar(player_vals, ideal_vals, labels):
                N = len(labels)
                angles = [n / float(N) * 2 * pi for n in range(N)]
                angles += angles[:1]

                player_vals += player_vals[:1]
                ideal_vals += ideal_vals[:1]

                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                ax.plot(angles, player_vals, linewidth=2, label="Player", color="blue")
                ax.fill(angles, player_vals, alpha=0.2, color="blue")
                ax.plot(angles, ideal_vals, linewidth=2, linestyle="dashed", label="Ideal", color="orange")
                ax.fill(angles, ideal_vals, alpha=0.2, color="orange")
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.set_title("Attribute Comparison", size=14)
                ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
                return fig

            player_vals = best_player[attribute_cols].tolist()
            ideal_vals = [ideal_attributes[attr] for attr in attribute_cols]
            radar_fig = plot_radar(player_vals.copy(), ideal_vals.copy(), attribute_cols)
            st.pyplot(radar_fig)

            # Mostrar atributos
            st.markdown(f"### {best_player['Name']} - Attributes")
            st.dataframe(best_player[attribute_cols].to_frame(), use_container_width=True)

        except Exception as e:
            st.error("⚠️ AI response error:")
            st.exception(e)
