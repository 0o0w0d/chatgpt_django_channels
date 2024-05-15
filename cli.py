import os
import openai

from dotenv import load_dotenv

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


# 상황극 설정
language = "English"
gpt_name = "Jjojjo"
level_string = f"a beginner in {language}"
level_word = "simple"
situation_en = "make new friends"
my_role_en = "me"
gpt_role_en = "new friend"

SYSTEM_PROMPT = (
    f"You are helpful assistant supporting people learning {language}. "
    f"Your name is {gpt_name}. "
    f"Please assume that the user you are assisting is {level_string}. "
    f"And please write only the sentence without the character role."
)

USER_PROMPT = (
    f"Let's have a conversation in {language}. "
    f"Please answer in {language} only "
    f"without providing a translation. "
    f"And please don't write down the pronunciation either. "
    f"Let us assume that the situation in '{situation_en}'. "
    f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
    f"Please make sure that I'm {level_string}, so please use {level_word} words "
    f"as much as possible. Now, start a conversation with the first sentence!"
)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


def gpt_query(user_query: str) -> str:
    """
    유저 메시지에 대해 gpt의 응답을 반환
    """

    global messages

    messages.append({"role": "user", "content": user_query})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    assistant_msg = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": assistant_msg})

    return assistant_msg


def main():
    # gpt로부터 초기 응답을 얻기 위한 코드
    assistant_msg = gpt_query(USER_PROMPT)
    print(f"[assistant] {assistant_msg}")

    while line := input("[user] ").strip():
        response = gpt_query(line)
        print(f"[assistant] {response}")


if __name__ == "__main__":
    main()
