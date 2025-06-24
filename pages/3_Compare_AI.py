import streamlit as st
import pandas as pd
import plotly.express as px
from ai.openai_client import call_openai_recommendations
import urllib.parse

# Load data
players_df = pd.read_csv("data/players_data.csv")

# UI
st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

description = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        try:
            # Get AI response
            recommendation_text, recommended_names = call_openai_recommendations(description, players_df)

            # Show report
            st.markdown("## ✨ AI Recommendation Report")
            st.markdown(recommendation_text)

            # Find both players in dataframe
            def get_player_by_name(name):
                return players_df[players_df["Name"] == name].iloc[0] if name in players_df["Name"].values else None

            player1 = get_player_by_name(recommended_names[0])
            player2 = get_player_by_name(recommended_names[1])

            # Show radar chart if both found
            if player1 is not None and player2 is not None:
                st.markdown("## 📊 Talent Evolution Comparison")

                radar_attributes = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical', 
                                    'Vision', 'Composure', 'Ball_Control']

                radar_df = pd.DataFrame({
                    'Attribute': radar_attributes,
                    player1["Name"]: [player1[attr] for attr in radar_attributes],
                    player2["Name"]: [player2[attr] for attr in radar_attributes]
                })

                radar_melted = radar_df.melt(id_vars="Attribute", var_name="Player", value_name="Score")
                fig = px.line_polar(radar_melted, r='Score', theta='Attribute', color='Player',
                                    line_close=True, range_r=[0, 100])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("One or both players could not be found in the dataset.")

        except Exception as e:
            st.error(f"AI response error: {e}")



