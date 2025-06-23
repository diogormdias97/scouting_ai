import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(user_prompt, system_msg):
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # versão gratuita
            messages=messages,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return str(e)

