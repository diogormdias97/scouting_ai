import os
import openai
import pandas as pd

# Garante que estás a usar a API moderna (openai >= 1.0.0)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_recommendations(prompt: str, df: pd.DataFrame) -> str:
    player_list = "\n".join(
        f"{row['Name']} ({row['Position']}, Age: {row['Age']}, Club: {row['Club']}, "
        f"Pace: {row['Pace']}, Dribbling: {row['Dribbling']}, Shooting: {row['Shooting']})"
        for _, row in df.iterrows()
    )

    full_prompt = (
        f"You are a professional football scouting assistant AI. "
        f"Based on the user's description of the ideal player, "
        f"recommend 2 to 3 players from the list provided below. "
        f"Only select players that appear in the list.\n\n"

        f"User Description:\n{prompt}\n\n"
        f"Available Players:\n{player_list}\n\n"

        f"For each recommended player, provide the following:\n"
        f"1. The player's name (must match exactly one in the list)\n"
        f"2. A short paragraph justifying why the player fits the user's criteria\n"
        f"3. The player’s strong points (attributes like pace, dribbling, etc.)\n"
        f"4. A short paragraph forecasting the player's potential evolution (e.g., how they might develop in 2–3 years)\n"
        f"5. A link to the player’s profile in the format: /Player_Profile?name=NAME_WITH_UNDERSCORES\n\n"

        f"Format the response exactly like this:\n"
        f"1. Name – Justification... Strong points: ... Forecast: ... [🔎 View Profile](link)\n"
        f"2. ..."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful football scouting assistant."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )

    return response.choices[0].message.content.strip()
