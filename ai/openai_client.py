import openai
import os

# Garante que a variável existe
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

openai.api_key = api_key

def generate_summary(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Input to generate_summary must be a string.")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a football scouting assistant."},
                {"role": "user", "content": f"Create a scouting report for a player with the following characteristics:\n{text}"}
            ],
            temperature=0.7,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")

