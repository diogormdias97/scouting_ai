# ai/openai_client.py
import os
import openai

# 1) ler a key do ambiente  (definida nos Secrets do Streamlit)
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai(user_prompt: str, system_msg: str) -> str:
    """
    Envia o prompt para o ChatCompletion e devolve apenas o conteúdo da resposta.
    """
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user",   "content": user_prompt}
    ]

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",   # usa o modelo que tiveres acesso
        messages=messages,
        temperature=0.4,
    )

    return resp.choices[0].message.content.strip()


