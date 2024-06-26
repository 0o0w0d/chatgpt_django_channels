from typing import List, TypedDict, Literal

from django.db import models
from django.conf import settings

from django.urls import reverse_lazy


class GptMessage(TypedDict):
    # role의 값은 "system", "user", "assistant"만
    role: Literal["system", "user", "assistant"]
    content: str


# 상황극 채팅방
class RolePlayingRoom(models.Model):

    # 언어 선택지
    class Language(models.TextChoices):
        # 식별자(key) / db 저장 값 / label (display)
        ENGLISH = "en-US", "English"
        JAPANESE = "ja-JP", "Japanese"
        CHINESE = "zh-CN", "Chinese"
        SPANISH = "es-ES", "Spanish"
        FRENCH = "fr-FR", "French"
        GERMAN = "de-DE", "German"
        RUSSIAN = "ru-RU", "Russian"

    class Level(models.IntegerChoices):
        BEGINNER = 1, "초급"
        ADVANCED = 2, "고급"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.ENGLISH,
        verbose_name="대화 언어",
    )
    level = models.SmallIntegerField(
        choices=Level.choices, default=Level.BEGINNER, verbose_name="레벨"
    )
    situation = models.CharField(max_length=100, verbose_name="상황")
    situation_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="상황 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, situation 필드를 번역해 자동 반영됩니다.",
    )
    my_role = models.CharField(max_length=100, verbose_name="내 역할")
    my_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="내 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, my_role 필드를 번역해 자동 반영됩니다.",
    )
    gpt_role = models.CharField(max_length=100, verbose_name="GPT 역할")
    gpt_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="GPT 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, gpt_role 필드를 번역해 자동 반영됩니다.",
    )

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return reverse_lazy("role_playing_room_detail", kwargs={"pk": self.pk})

    def get_initial_messages(self) -> List[GptMessage]:
        gpt_name = "RolePlayingBot"
        language = self.get_language_display()
        situation_en = self.situation_en
        my_role_en = self.my_role_en
        gpt_role_en = self.gpt_role_en

        if self.level == self.Level.BEGINNER:
            level_string = f"a beginner in {language}"
            level_word = "simple"
        elif self.level == self.Level.ADVANCED:
            level_string = f"a advanced learner in {language}"
            level_word = "advanced"
        else:
            raise ValueError(f"Invaild level: {self.level}")

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

        return [
            # 오타 체크를 위해 GptMessage class 사용
            # {"role": "system", "content": SYSTEM_PROMPT},
            # {"role": "user", "content": USER_PROMPT},
            GptMessage(role="system", content=SYSTEM_PROMPT),
            GptMessage(role="user", content=USER_PROMPT),
        ]

    def get_recommend_message(self) -> str:
        """
        맥락에 맞는 메시지를 추천해달라는 문장을 return
        """

        level = self.level

        if level == self.Level.BEGINNER:
            level_word = "simple"
        elif level == self.Level.ADVANCED:
            level_word = "advanced"
        else:
            raise ValueError(f"Invalid level : {level}")

        return (
            f"Can you please provide me an {level_word} example "
            f"of how to respond to the last sentence "
            f"in this situation, without providing a translation "
            f"and any introductory phrases or sentences."
        )
