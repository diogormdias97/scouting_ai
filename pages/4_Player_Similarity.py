import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load player data
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ["Pace", "Shooting", "Passing", "Dribbling", "Defending",
                  "Physical", "Vision", "Composure", "Ball_Control"]

# Sidebar
st.title("🧬 Player Similarity")
selected_player = st.selectbox("Choose a player", sorted(players_df["Name"].unique()))

# Compute similarity
selected_vector = players_df[players_df["Name"] == selected_player][attribute_cols].values
others_df = players_df[players_df["Name"] != selected_player].copy()
others_df["Similarity"] = cosine_similarity(others_df[attribute_cols], selected_vector)

# Show top similar players
top_similar = others_df.sort_values("Similarity", ascending=False).head(5)
st.markdown("### 🔍 Most Similar Players")
st.table(top_similar[["Name", "Position", "Age", "Similarity"]])
