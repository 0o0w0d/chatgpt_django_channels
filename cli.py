import os
import openai

from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO
from tempfile import NamedTemporaryFile
import pygame

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

RECOMMEND_PROMPT = (
    f"Can you please provide me an {level_word} example "
    f"of how to respond to the last sentence "
    f"in this situation, without providing a translation "
    f"and any introductory phrases or sentences."
)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


def gpt_query(user_query: str, skip_save: bool = False) -> str:
    """
    유저 메시지에 대해 gpt의 응답을 반환
    """

    global messages

    messages.append({"role": "user", "content": user_query})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    assistant_msg = response["choices"][0]["message"]["content"]

    if skip_save is False:
        messages.append({"role": "assistant", "content": assistant_msg})

    return assistant_msg


# 지정 경로의 오디오 파일을 재생하기 위한 함수
def play_file(file_path: str) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # audio가 재생되는 동안 기다리기
    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.quit()


# 음성으로 메시지를 읽어주는 코드
def say(message: str, lang: str) -> None:

    # 메모리 객체에 저장하기 위해서 BytesIO 사용
    io = BytesIO()
    # write_to_fp : 인자로 지정한 파일 객체에 음성 파일 저장
    gTTS(message, lang=lang).write_to_fp(io)

    # 임시 파일 생성
    with NamedTemporaryFile(
        delete=False
    ) as f:  # 자동 삭제되지 않도록 delete=False 지정
        f.write(io.getvalue())
        f.close()

        play_file(f.name)
        os.remove(f.name)


def main():

    # gpt로부터 초기 응답을 얻기 위한 코드
    assistant_msg = gpt_query(USER_PROMPT)
    print(f"[assistant] {assistant_msg}")

    """
        !recommend: 표현 추천
        !say: 메시지 음성으로 읽어주기
    """

    while line := input("[user] ").strip():

        if line == "!recommend":
            # !recommand의 경우 GPT 응답을 messages에 저장하지 않기 위해 skip_save=True 적용
            recommend_msg = gpt_query(RECOMMEND_PROMPT, skip_save=True)
            print("추천 표현: ", recommend_msg)
            pass

        elif line == "!say":
            say(messages[-1]["content"], "en")
        else:
            response = gpt_query(line)
            print(f"[assistant] {response}")


if __name__ == "__main__":
    main()
