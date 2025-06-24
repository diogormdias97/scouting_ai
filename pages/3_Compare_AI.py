import streamlit as st
import pandas as pd
import numpy as np
import re
import urllib.parse
import plotly.graph_objects as go
from ai.openai_client import call_openai_recommendations

players_df = pd.read_csv("data/players_data.csv")

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

description = st.text_area("🗣️ Describe your ideal player", "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        try:
            ai_response = call_openai_recommendations(description, players_df)
            st.markdown("## ✨ AI Recommendation Report")

            pattern = r"\d+\.\s*(.+?)\s*-\s*(.+?)\s*Strong points:\s*(.+)"
            matches = re.findall(pattern, ai_response, re.DOTALL)

            recommended_names = []
            for name, desc, strong in matches:
                name_clean = name.strip()
                encoded = urllib.parse.quote(name_clean)
                st.markdown(f"**{name_clean}** - {desc.strip()} **Strong points:** {strong.strip()} [🔎 View Profile](/Player_Profile?name={encoded})")
                recommended_names.append(name_clean)

            # Show radar if 2 valid players matched
            if len(recommended_names) == 2:
                player1 = players_df[players_df["Name"] == recommended_names[0]].iloc[0]
                player2 = players_df[players_df["Name"] == recommended_names[1]].iloc[0]
                attributes = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical",
                              "Vision", "Composure", "Ball_Control"]
                
                fig = go.Figure()

                fig.add_trace(go.Scatterpolar(
                    r=[player1[attr] for attr in attributes],
                    theta=attributes,
                    fill='toself',
                    name=player1["Name"]
                ))

                fig.add_trace(go.Scatterpolar(
                    r=[player2[attr] for attr in attributes],
                    theta=attributes,
                    fill='toself',
                    name=player2["Name"]
                ))

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=True,
                    title="🧠 Talent Evolution – Attribute Comparison"
                )

                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"AI response error: {e}")



