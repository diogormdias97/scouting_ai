import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai_recommendations(user_prompt: str) -> str:
    system_message = (
        "You are a football scout assistant. Based on the user's prompt, you must recommend 3 players "
        "with the highest potential match. For each player, output a recommendation in Markdown format "
        "including their name, a short paragraph about why they fit, and their profile link using:\n"
        "`[🔗 View Profile](./Player_Profile?name=NAME)` (replace NAME with the actual name, use %20 for spaces).\n"
        "End your message directly after the third recommendation. Be concise and professional."
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    return response['choices'][0]['message']['content'].strip()
