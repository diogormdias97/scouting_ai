import os
import openai
import pandas as pd

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_recommendations(prompt: str, df: pd.DataFrame) -> list:
    player_list = "\n".join(
        f"{row['Name']} ({row['Position']}, Age: {row['Age']}, Club: {row['Club']}, "
        f"Pace: {row['Pace']}, Dribbling: {row['Dribbling']}, Shooting: {row['Shooting']})"
        for _, row in df.iterrows()
    )

    full_prompt = (
        f"You are a football scout assistant AI. Based on the user description below, "
        f"suggest 2 players from the list of known players. Only use names that appear in the list.\n\n"
        f"User Description:\n{prompt}\n\n"
        f"Available Players:\n{player_list}\n\n"
        f"For each recommended player, provide:\n"
        f"- Name (must match exactly one from the list)\n"
        f- "Short paragraph justifying the recommendation\n"
        f"- Strong points\n"
        f"- Profile link in format: /Player_Profile?name=NAME_WITH_UNDERSCORES\n"
        f"- Then say: 'Based on technical attributes and age, [Name] shows high growth potential.'\n"
        f"Output format:\n"
        f"1. Name - Description... Strong points: ... [🔎 View Profile](/Player_Profile?name=...). Talent Evolution: ...\n"
        f"2. ..."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful scouting assistant."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip().split("\n")
