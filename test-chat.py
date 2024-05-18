import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# python-dotenv 라이브러리를 활용해 현재 경로의 .env 파일을 환경변수로서 로딩
from dotenv import load_dotenv

load_dotenv()


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "당신은 영어 학습을 도와주는 챗봇입니다."},
        {"role": "user", "content": "대화를 나눠봅시다."},
    ],
)

print(response)
print(response.choices[0].message.content)
