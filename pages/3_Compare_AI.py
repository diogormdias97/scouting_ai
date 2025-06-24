import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from math import pi
import openai
import json

# --- CONFIGURAÇÕES ---
st.set_page_config(page_title="Compare AI", layout="wide")

# --- CHAVE OPENAI (usa a tua ou define via secrets) ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "sk-..."

# --- CARREGAR DADOS ---
players_df = pd.read_csv("data/players_data.csv")
attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                  'Physical', 'Vision', 'Composure', 'Ball_Control']

# --- TÍTULO E INSTRUÇÕES ---
st.title("🎯 AI Player Finder")
st.markdown("Describe the type of player you're looking for, and our AI will recommend the closest match!")

# --- INPUT DO UTILIZADOR ---
user_prompt = st.text_area("🗣️ Describe your ideal player", 
    "I'm looking for a fast and agile left winger under 17, with great dribbling and high pace.")

# --- FUNÇÃO PARA CHAMAR OPENAI ---
def call_openai(user_prompt):
    system_msg = (
        "You are a football scouting assistant. Based on the user's prompt, "
        "return the ideal attribute profile (scale 0-100) for the following attributes only: "
        "Pace, Shooting, Passing, Dribbling, Defending, Physical, Vision, Composure, Ball_Control. "
        "Only return a JSON object, like:\n"
        '{"Pace": 90, "Shooting": 75, ..., "Ball_Control": 85}'
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_msg},
                  {"role": "user", "content": user_prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

# --- BOTÃO DE COMPARAÇÃO ---
if st.button("🔍 Find Player"):
    with st.spinner("Asking AI and finding the best match..."):
        try:
            ideal_json = call_openai(user_prompt)
            st.markdown("#### Raw AI Output")
            st.code(ideal_json)

            ideal_attributes = json.loads(ideal_json)
            ideal_vector = np.array([ideal_attributes[attr] for attr in attribute_cols]).reshape(1, -1)

            # Calcular similaridade com todos os jogadores
            player_vectors = players_df[attribute_cols].values
            similarities = cosine_similarity(ideal_vector, player_vectors)[0]
            best_idx = np.argmax(similarities)
            best_player = players_df.iloc[best_idx]

            # Mostrar resultado
            st.success(f"🏅 Best Match: **{best_player['Name']}** ({best_player['Club']}, {best_player['Age']} yrs, {best_player['Position']})")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔧 Ideal Profile (AI)")
                st.write(pd.DataFrame([ideal_attributes]))

            with col2:
                st.subheader("📋 Best Match Profile")
                st.write(best_player[attribute_cols])

            # Radar chart
            def plot_radar(player_vals, ideal_vals, labels):
                N = len(labels)
                angles = [n / float(N) * 2 * pi for n in range(N)]
                angles += angles[:1]
                player_vals += player_vals[:1]
                ideal_vals += ideal_vals[:1]

                fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                ax.plot(angles, player_vals, linewidth=2, label="Player")
                ax.fill(angles, player_vals, alpha=0.3)
                ax.plot(angles, ideal_vals, linewidth=2, linestyle="dashed", label="AI Ideal")
                ax.fill(angles, ideal_vals, alpha=0.2)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels)
                ax.legend(loc="upper right")
                return fig

            player_vals = best_player[attribute_cols].tolist()
            ideal_vals = [ideal_attributes[attr] for attr in attribute_cols]

            st.subheader("📊 Attribute Comparison (Radar)")
            fig = plot_radar(player_vals.copy(), ideal_vals.copy(), attribute_cols)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"AI response error: {e}")
