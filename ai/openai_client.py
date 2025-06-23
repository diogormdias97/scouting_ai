import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(player_name, stats_dict):
    prompt = f"""
    You are a football scout assistant. Based on the following stats, write a short scouting report for the player named {player_name}.

    Stats:
    {stats_dict}

    The report should mention strengths, weaknesses, and potential.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful football scout assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=250
    )

    return response['choices'][0]['message']['content']
