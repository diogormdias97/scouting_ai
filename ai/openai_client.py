import os
import streamlit as st
from openai import OpenAI

# Inicializar cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # ou usa os.environ.get(...)

def call_openai_recommendations(user_prompt, player_names):
    system_msg = (
        "You are an AI football analyst. Your task is to suggest 2 or 3 players from the provided list "
        "who best match the user's description. For each recommendation, explain:\n"
        "- Why the player fits the prompt;\n"
        "- Their main strengths (based on attributes);\n"
        "- A short summary of their profile.\n"
        "Respond in markdown format using bullet points. Each player should be presented like this:\n"
        "**Player Name**: short explanation.\n"
        "Include `[🔍 View Profile](link)` where `link` is `/Player_Profile?name=Player%20Name`\n"
        "Only use players from this list: " + ", ".join(player_names)
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            max_tokens=900
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI response error: {e}"
