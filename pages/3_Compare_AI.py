import streamlit as st
import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from math import pi
from ai.openai_client import call_openai

# Load data
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

st.set_page_config(page_title="AI Player Finder", layout="wide")
st.title("🎯 AI Player Finder")

st.markdown("Describe the ideal player profile. The AI will match and compare the closest real players.")

# Input from user
user_prompt = st.text_area("🗣️ Describe your ideal player", "Fast winger with strong dribbling and finishing under 17 years old.")

if st.button("🔍 Compare Players"):
    with st.spinner("🧠 Asking AI and comparing attributes..."):
        system_msg = (
            "You are a football scout assistant. Based on the user's prompt, return a JSON with the ideal values (0–100 scale) for: "
            "Pace, Shooting, Passing, Dribbling, Defending, Physical, Vision, Composure, Ball_Control. "
            "Output ONLY the JSON like: {\"Pace\": 90, ...}"
        )
        ideal_json = call_openai(user_prompt, system_msg)

        try:
            ideal_attributes = json.loads(ideal_json)
            ideal_vector = np.array([ideal_attributes[attr] for attr in attribute_cols]).reshape(1, -1)
            player_vectors = players_df[attribute_cols].values

            similarities = cosine_similarity(ideal_vector, player_vectors)[0]
            players_df["Similarity"] = similarities

            top_matches = players_df.sort_values("Similarity", ascending=False).head(5)
            st.success("✅ Top Matches Found")
            st.dataframe(top_matches[["Name", "Club", "Age", "Position", "Similarity"] + attribute_cols])

            # Show radar charts for top 3
            def plot_radar(player_vals, ideal_vals, labels, player_name):
                N = len(labels)
                angles = [n / float(N) * 2 * pi for n in range(N)]
                angles += angles[:1]
                player_vals += player_vals[:1]
                ideal_vals += ideal_vals[:1]

                fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
                ax.plot(angles, player_vals, label=player_name)
                ax.fill(angles, player_vals, alpha=0.2)
                ax.plot(angles, ideal_vals, linestyle="dashed", label="Ideal")
                ax.fill(angles, ideal_vals, alpha=0.2)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.legend(loc="upper right")
                return fig

            st.markdown("### 🔍 Visual Attribute Comparison")
            ideal_vals = [ideal_attributes[attr] for attr in attribute_cols]

            for _, row in top_matches.iterrows():
                st.subheader(row["Name"])
                player_vals = row[attribute_cols].tolist()
                fig = plot_radar(player_vals, ideal_vals, attribute_cols, row["Name"])
                st.pyplot(fig)

            # Attribute Gaps
            st.markdown("### 🔬 Attribute Differences")
            for _, row in top_matches.iterrows():
                st.write(f"**{row['Name']}** - Attribute Gaps:")
                gaps = {attr: ideal_attributes[attr] - row[attr] for attr in attribute_cols}
                gaps_df = pd.DataFrame(gaps.items(), columns=["Attribute", "Gap"])
                st.dataframe(gaps_df.sort_values("Gap", key=abs, ascending=False))

        except Exception as e:
            st.error(f"AI response error: {e}")
            st.text_area("Raw AI Output", ideal_json)


