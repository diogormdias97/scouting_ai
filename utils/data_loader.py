import pandas as pd
import streamlit as st

@st.cache_data
def load_players():
    return pd.read_csv("data/players_data.csv")

@st.cache_data
def load_games():
    return pd.read_csv("data/games.csv")

