import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
from ai.openai_client import call_openai_recommendations
import plotly.graph_objects as go

# Load data
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control', 'Avg_Rating']

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

description = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        try:
            recommendations = call_openai_recommendations(description, players_df)
            st.markdown("## ✨ AI Recommendation Report")

            selected_names = []

            for i, line in enumerate(recommendations):
                if not line.strip():
                    continue
                try:
                    name = line.split(" - ")[0].strip()
                    encoded_name = urllib.parse.quote(name)
                    profile_link = f"/Player_Profile?name={encoded_name}"
                    line_with_link = f"{line.split('[🔎')[0]} [🔎 View Profile]({profile_link})"
                    st.markdown(f"{i+1}. {line_with_link}")
                    selected_names.append(name)
                except:
                    continue

            # Radar comparison
            if len(selected_names) == 2:
                st.markdown("## 📊 Attribute Comparison")
                player1 = players_df[players_df["Name"] == selected_names[0]].iloc[0]
                player2 = players_df[players_df["Name"] == selected_names[1]].iloc[0]

                values1 = [player1[attr] for attr in attribute_cols]
                values2 = [player2[attr] for attr in attribute_cols]

                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values1,
                    theta=attribute_cols,
                    fill='toself',
                    name=selected_names[0]
                ))
                fig.add_trace(go.Scatterpolar(
                    r=values2,
                    theta=attribute_cols,
                    fill='toself',
                    name=selected_names[1]
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"AI response error: {e}")


