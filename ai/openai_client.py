import streamlit as st
from openai import OpenAI
from urllib.parse import quote

# Pega chave da secret store do Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def call_openai_recommendations(user_prompt, player_names):
    system_msg = (
        "You are an AI football scout assistant. Your job is to recommend 2 or 3 players from the provided list "
        "that best match the user's description.\n\n"
        "For each recommendation, include:\n"
        "- Player's name\n"
        "- Explanation of why they fit the profile\n"
        "- 2-3 strong attributes (based on football qualities)\n"
        "- A profile link in the format: `/Player_Profile?name=Player%20Name`\n\n"
        f"Only choose from this list of players: {', '.join(player_names)}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI response error: {e}"

