"""DiceBear에 요청하여 아바타 SVG를 가져오는 모듈."""
import requests
import xml.etree.ElementTree as ET

STYLES = {"픽셀 주민": "pixel-art", "로봇 주민": "bottts"}
API_VERSION = "10.x"


def get_avatar(seed, style):
    seed = seed.strip()
    if not seed or len(seed) > 20:
        raise ValueError("닉네임은 1~20자로 입력해 주세요.")
    if style not in STYLES.values():
        raise ValueError("지원하지 않는 스타일입니다.")
    try:
        response = requests.get(
            f"https://api.dicebear.com/{API_VERSION}/{style}/svg",
            params={"seed": seed}, timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError("주민 사진을 가져오지 못했어요. 인터넷 연결을 확인하고 다시 시도해 주세요.") from error
    # 이미지 요청의 응답은 JSON이 아니라 SVG 텍스트이다.
    try:
        root = ET.fromstring(response.text)
        if root.tag.split("}")[-1] != "svg":
            raise ValueError()
    except (ET.ParseError, ValueError) as error:
        raise ValueError("API가 올바른 SVG 이미지를 보내지 않았어요.") from error
    return response.text
