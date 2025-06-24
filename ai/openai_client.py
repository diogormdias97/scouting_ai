from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_recommendations(user_prompt: str) -> str:
    system_message = (
        "You are a football scout assistant. Based on the user's prompt, you must recommend 2-3 youth players "
        "with the highest potential match. For each player, write a short paragraph explaining why, "
        "and include a profile link using the format: [🔗 View Profile](./Player_Profile?name=PLAYER%20NAME)."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
