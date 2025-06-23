import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(content):
    prompt = f"You are a football analyst. Analyze the player stats:\n\n{content}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a football analyst"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
