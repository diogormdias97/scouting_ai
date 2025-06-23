import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai(prompt: str, system_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=250
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

