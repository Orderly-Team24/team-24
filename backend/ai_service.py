from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

with open("../prompts/system_prompt.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def recommend(menu_text, user_preferences):

    response = client.chat.completions.create(
        model="qwen/qwen3.5-9b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content":
                f"""
                Menu:
                {menu_text}

                User Preferences:
                {user_preferences}
                """
            }
        ]
    )

    return response.choices[0].message.content
