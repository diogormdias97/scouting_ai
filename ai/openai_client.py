import openai
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]  # ou define manualmente

def call_openai_recommendations(user_prompt, players_df):
    attribute_cols = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending',
                      'Physical', 'Vision', 'Composure', 'Ball_Control']

    system_msg = (
        "És um olheiro de futebol. Com base na descrição fornecida, "
        "seleciona 2 ou 3 jogadores do dataset (com os nomes disponíveis na lista JSON abaixo) "
        "que melhor se adequem ao perfil pretendido. "
        "Usa apenas os nomes fornecidos e escreve um relatório com recomendações detalhadas.\n\n"
        "Formato de resposta obrigatório:\n"
        "[\n"
        "  {\"name\": \"Nome1\", \"reason\": \"Explica por que este jogador é recomendado.\"},\n"
        "  {\"name\": \"Nome2\", \"reason\": \"...\"}\n"
        "]\n\n"
        "Lista de jogadores disponíveis:\n" + json.dumps(players_df['Name'].tolist())
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6
    )

    return response.choices[0].message.content
