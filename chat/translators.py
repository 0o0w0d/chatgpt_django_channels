# 용이한 크롤링을 위해 구글 번역 모바일 페이지 크롤링

from typing import Literal

import requests
from bs4 import BeautifulSoup


def google_translate(
    text: str, source: Literal["auto", "en", "ko"], target: Literal["en", "ko"]
) -> str:
    """
    text: 번역할 내용
    source: 입력받는 언어
    target: 번역할 언어
    """

    text = text.strip()
    if not text:
        return ""

    # 크롤링할 주소
    endpoint_url = "https://translate.google.com/m"

    # QueryString 인자
    # https://translate.google.com/m?sl=ko&tl=en&hl=ko&q=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94
    params = {
        "hl": source,
        "sl": source,
        "tl": target,
        "q": text,
        "ie": "UTF-8",
        "prev": "_m",
    }

    # mobile device header 형식
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
        )
    }

    # GET 요청
    res = requests.get(endpoint_url, params=params, headers=headers, timeout=5)

    # status_code != 200: raise error
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # 번역된 내용이 페이지의 result-container 클래스에 위치
    translated_text = soup.select_one(".result-container").text.strip()

    return translated_text
