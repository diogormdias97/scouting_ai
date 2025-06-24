import streamlit as st
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from math import pi
from sklearn.metrics.pairwise import cosine_similarity
from ai.openai_client import call_openai

# === Dados ===
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

# === Página ===
st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for. Our AI will recommend the best match and show you a comparison.")

# === Input ===
user_prompt = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and strong forward, with great dribbling and shooting.")

if st.button("🔍 Find Player"):
    with st.spinner("🎯 Calling AI and comparing players..."):

        system_msg = (
            "You are a football scout assistant. Based on the user's prompt, "
            "return a JSON object with numeric values (0-100) for these attributes: "
            "Pace, Shooting, Passing, Dribbling, Defending, Physical, Vision, Composure, Ball_Control. "
            "Example: {\"Pace\": 85, \"Shooting\": 80, ..., \"Ball_Control\": 90}. Do not include text, just pure JSON."
        )

        try:
            ideal_json = call_openai(user_prompt, system_msg)
            ideal_attributes = json.loads(ideal_json)

            if not all(attr in ideal_attributes for attr in attribute_cols):
                missing = [attr for attr in attribute_cols if attr not in ideal_attributes]
                st.error(f"⚠️ Missing attributes in AI output: {missing}")
                st.json(ideal_json)
                st.stop()

            ideal_vector = np.array([ideal_attributes[attr] for attr in attribute_cols]).reshape(1, -1)
            player_vectors = players_df[attribute_cols].values
            similarities = cosine_similarity(ideal_vector, player_vectors)[0]
            best_idx = np.argmax(similarities)
            best_player = players_df.iloc[best_idx]

            st.success(f"🏅 Best match: **{best_player['Name']}** ({best_player['Club']}, {best_player['Age']} yrs)")

            # === Radar Chart ===
            def plot_radar(player_vals, ideal_vals, labels, player_name):
                N = len(labels)
                angles = [n / float(N) * 2 * pi for n in range(N)]
                angles += angles[:1]

                player_vals += [player_vals[0]]
                ideal_vals += [ideal_vals[0]]

                fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
                ax.plot(angles, player_vals, label=player_name)
                ax.fill(angles, player_vals, alpha=0.25)
                ax.plot(angles, ideal_vals, linestyle='dashed', label="Ideal")
                ax.fill(angles, ideal_vals, alpha=0.25)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.2))
                return fig

            player_vals = best_player[attribute_cols].tolist()
            ideal_vals = [ideal_attributes[attr] for attr in attribute_cols]
            radar_fig = plot_radar(player_vals.copy(), ideal_vals.copy(), attribute_cols, best_player['Name'])
            st.pyplot(radar_fig)

            # === Raw output (debugging/curiosidade) ===
            st.subheader(best_player["Name"])
            st.markdown("#### Raw AI Output")
            st.json(ideal_attributes)

        except json.JSONDecodeError:
            st.error("❌ The AI did not return valid JSON.")
            st.text(ideal_json)
        except Exception as e:
            st.error(f"AI response error: {e}")
            st.text(ideal_json)

