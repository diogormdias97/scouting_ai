import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ai.openai_client import generate_summary

# Título da página
st.title("📊 Game-by-game Stats")

# Leitura do ficheiro CSV
try:
    games_df = pd.read_csv("data/games.csv")
except FileNotFoundError:
    st.error("O ficheiro 'data/games.csv' não foi encontrado.")
    st.stop()

# Seletor de jogador
player_names = games_df['Name'].unique()
selected_player = st.selectbox("Select a Player", player_names)

# Filtrar os dados do jogador selecionado
player_data = games_df[games_df['Player'] == selected_player]

# Mostrar atributos médios
st.subheader("⚙️ Player Attributes")
attributes = ['Goals', 'Assists', 'Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
              'Physical', 'Vision', 'Composure', 'Ball_Control']
attribute_values = player_data[attributes].mean().round(0).astype(int)
attribute_df = pd.DataFrame(attribute_values, columns=['Value']).reset_index()
attribute_df.columns = ['Attribute', 'Value']
st.table(attribute_df)

# Gráfico Radar
st.subheader("📈 Radar Chart")
try:
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=attribute_df['Value'],
        theta=attribute_df['Attribute'],
        fill='toself',
        name=selected_player
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 20])
        ),
        showlegend=False
    )

    st.plotly_chart(fig)
except ImportError:
    st.warning("Plotly não está instalado. O gráfico radar não pode ser exibido.")

# 📄 Relatório com IA
st.subheader("🧠 AI Report")

if st.button("Generate Report"):
    try:
        summary_input = "\n".join([
            f"{attr}: {value}" for attr, value in attribute_values.items()
        ])
        summary = generate_summary(summary_input)
        st.success("AI summary generated successfully!")
        st.write(summary)
    except Exception as e:
        st.error(f"Error generating AI summary: {e}")
        


