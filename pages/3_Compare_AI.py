import streamlit as st
import pandas as pd
import urllib.parse
import plotly.express as px
from ai.openai_client import call_openai_recommendations

# === Carregamento de dados ===
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

# === Título e descrição ===
st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

description = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

if st.button("🔍 Find Player"):
    with st.spinner("Asking AI for recommendations..."):
        try:
            recommendation_text, recommended_names = call_openai_recommendations(description, players_df)

            st.markdown("## ✨ AI Recommendation Report")
            st.markdown(recommendation_text, unsafe_allow_html=True)

            # === Comparação Gráfica (Talent Evolution) ===
            if len(recommended_names) >= 2:
                player1 = players_df[players_df["Name"] == recommended_names[0]].iloc[0]
                player2 = players_df[players_df["Name"] == recommended_names[1]].iloc[0]

                st.markdown("## 📊 Talent Evolution Comparison")

                # Texto de comparação antes do gráfico
                avg1 = sum([player1[attr] for attr in attribute_cols]) / len(attribute_cols)
                avg2 = sum([player2[attr] for attr in attribute_cols]) / len(attribute_cols)
                best_player = player1["Name"] if avg1 >= avg2 else player2["Name"]
                diff = round(abs(avg1 - avg2), 1)

                st.markdown(
                    f"Before diving into the radar chart, it's important to highlight that based on the overall technical profile, "
                    f"**{best_player}** has a slightly stronger average attribute score (difference of {diff} points). "
                    f"This suggests a potentially better alignment with the user’s criteria, but both players showcase excellent potential. "
                    f"The following chart offers a side-by-side view of their main skills."
                )

                # Dados para radar
                radar_df = pd.DataFrame({
                    "Attribute": attribute_cols,
                    player1["Name"]: [player1[attr] for attr in attribute_cols],
                    player2["Name"]: [player2[attr] for attr in attribute_cols]
                })

                radar_df = radar_df.melt(id_vars=["Attribute"], var_name="Player", value_name="Score")
                fig = px.line_polar(radar_df, r="Score", theta="Attribute", color="Player", line_close=True, range_r=[0, 100])
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"AI response error: {e}")



