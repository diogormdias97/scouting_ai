import streamlit as st
import pandas as pd
from ai.openai_client import call_openai_recommendations

st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest matches!")

players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision


