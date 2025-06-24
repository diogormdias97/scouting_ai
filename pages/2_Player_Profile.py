import streamlit as st
import pandas as pd
import urllib.parse

# Load data
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control', 'Avg_Rating']

# Obter parâmetro da query string
query_params = st.query_params.to_dict()
selected_name = query_params.get("name", None)

if selected_name:
    selected_name = urllib.parse.unquote(selected_name)
else:
    selected_name = players_df.iloc[0]["Name"]  # default fallback

st.title("🧍 Player Profile")

# Dropdown de navegação também permite mudar jogador
name_list = players_df["Name"].dropna().unique().tolist()
name = st.selectbox("Select a player", name_list, index=name_list.index(selected_name))

# Atualiza URL quando se muda manualmente
if name != selected_name:
    st.experimental_set_query_params(name=name)

# Extrair os dados do jogador
player_row = players_df[players_df["Name"] == name].iloc[0]

# Mostrar info básica
st.subheader(f"{name}")
st.markdown(f"""
**Position:** {player_row['Position']} | **Foot:** {player_row['Foot']}  
**Age:** {player_row['Age']} | **Height:** {player_row['Height']} cm | **Weight:** {player_row['Weight']} kg
""")

# Mostrar atributos
st.subheader("⚽ Attributes")
st.bar_chart(player_row[attribute_cols])
