import openai
import os
import pandas as pd

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_recommendations(prompt: str, df: pd.DataFrame):
    player_list = "\n".join(
        f"{row['Name']} ({row['Position']}, Age: {row['Age']}, Club: {row['Club']}, "
        f"Pace: {row['Pace']}, Dribbling: {row['Dribbling']})"
        for _, row in df.iterrows()
    )

    full_prompt = (
        "You're a football scouting assistant AI. Based on the user request below, recommend 2 players "
        "from the available list (only players from the list). Use the name **exactly** as written in the list.\n\n"
        f"User Request:\n{prompt}\n\nAvailable Players:\n{player_list}\n\n"
        "Return a markdown formatted list with:\n"
        "1. Name - Description. Strong points: ..., ... 🔎 View Profile\n"
        "2. Name - Description. Strong points: ..., ... 🔎 View Profile"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a football scouting assistant."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
        max_tokens=700
    )

    content = response.choices[0].message.content.strip()

    # Extract names from start of lines (1. Name - ...)
    lines = content.splitlines()
    recommended_names = []
    for line in lines:
        if line.strip().startswith("1.") or line.strip().startswith("2."):
            name_part = line.split("-")[0].replace("1.", "").replace("2.", "").strip()
            recommended_names.append(name_part)

    return content, recommended_names
