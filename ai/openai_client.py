import streamlit as st
from openai import OpenAI
from urllib.parse import quote

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # ou usa os.environ.get(...)

def call_openai_recommendations(user_prompt, player_names):
    system_msg = (
        "You are an AI football scout assistant. Your goal is to recommend 2 or 3 players from the provided list "
        "that best match the user's description.\n\n"
        "Respond ONLY with a short markdown report. For each recommended player, include:\n"
        "- **Player name**\n"
        "- Why the player fits the request\n"
        "- Main strengths based on the attributes\n"
        "- A link to their profile page in the format: `/Player_Profile?name=Player%20Name` (URL encoded)\n\n"
        f"Only use players from this list: {', '.join(player_names)}"
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
