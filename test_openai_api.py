import os
import openai

from dotenv import load_dotenv

load_dotenv()


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# openai.api_key = os.getenv("OPENAI_API_KEY")

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="""
    Fix grammar errors:
    - I is a boy
    - You is a girls""".strip(),
)

print("test #1")
print(response)
print("응답 ::", response.choices[0].text.strip())

print("--------------------------------")


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "당신은 지식이 풍부한 도우미입니다."},
        {"role": "user", "content": "세계에서 가장 큰 도시는 어디인가요?"},
    ],
)

print("test #2")
print(response)
print("응답 ::", response.choices[0].message.content)
