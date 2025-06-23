import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a football analyst assistant."},
            {"role": "user", "content": f"Create a scouting report based on the following attributes:\n{text}"}
        ],
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']
