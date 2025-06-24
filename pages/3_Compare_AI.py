import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from math import pi
from ai.openai_client import call_openai_recommendations

st.set_page_config(page_title="Compare AI", layout="wide")

# --- Load data ---
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

# --- App UI ---
st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest match!")

user_prompt = st.text_area("🗣️ Describe your ideal player",
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking the AI and comparing players..."):
        try:
            ai_response = call_openai_recommendations(user_prompt, players_df)
            recommendations = eval(ai_response)  # JSON list of dicts

            for rec in recommendations:
                name = rec['name']
                reason = rec['reason']
                player = players_df[players_df["Name"] == name]

                if not player.empty:
                    player_info = player.iloc[0]

                    # Link to profile
                    profile_link = f"/Player_Profile?name={name.replace(' ', '%20')}"

                    # Show result
                    st.markdown(f"### **{name}**")
                    st.markdown(f"📋 {reason}")
                    st.markdown(f"[🔗 View Profile]({profile_link})")

                    # Radar Chart
                    def plot_radar(player_vals, labels):
                        N = len(labels)
                        angles = [n / float(N) * 2 * pi for n in range(N)]
                        angles += angles[:1]
                        player_vals += player_vals[:1]

                        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
                        ax.plot(angles, player_vals, linewidth=2, label=name)
                        ax.fill(angles, player_vals, alpha=0.3)
                        ax.set_xticks(angles[:-1])
                        ax.set_xticklabels(labels)
                        return fig

                    vals = player_info[attribute_cols].tolist()
                    radar_fig = plot_radar(vals, attribute_cols)
                    st.pyplot(radar_fig)
                else:
                    st.warning(f"⚠️ Player `{name}` not found in database.")

        except Exception as e:
            st.error(f"AI response error: {e}")
            st.code(ai_response if 'ai_response' in locals() else "No response.")

