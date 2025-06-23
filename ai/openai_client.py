import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # carrega a API key se estiver num ficheiro .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(user_prompt, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # ou outro que tenhas acesso
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()
