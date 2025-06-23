import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from ai.openai_client import generate_summary

st.title("📊 Player Profile")

# Carregar os dados dos jogadores
df = load_data()

# Selecionar jogador
player_names = df['Name'].unique()
selected_player = st.selectbox("Select a player", player_names)

# Obter dados do jogador
player_data = df[df['Name'] == selected_player].iloc[0]

# Mostrar atributos
st.subheader("Attributes")
attributes = ['Goals', 'Assists', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
              'Physical', 'Vision', 'Composure', 'Ball_Control']

attr_data = player_data[attributes]

st.dataframe(attr_data.to_frame(name="Value"))

# Estatísticas por jogo (carregar outro CSV)
try:
    games_df = pd.read_c

