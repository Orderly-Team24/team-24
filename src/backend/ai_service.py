from openai import OpenAI
from retriever import search_food


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


def get_recommendation(user_message):

    # 1. Search food database
    foods = search_food(user_message)

    context = "\n\n".join(
        [food.page_content for food in foods]
    )


    # 2. Send retrieved information to Qwen
    response = client.chat.completions.create(
    model="qwen/qwen3.5-9b",
    messages=[
        {
            "role": "system",
            "content": "You are Orderly, a food recommendation AI. Recommend meals based on user needs."
        },
        {
            "role": "user",
            "content": f"""
Available food options:

{context}

User request:
{user_message}

Recommend the best option.
"""
        }
    ],
    temperature=0.7
)

    return response.choices[0].message.content