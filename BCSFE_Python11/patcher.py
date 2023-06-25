"""Handler for patching save data"""

import hashlib
from typing import Union
import requests


def get_md5_sum(data: bytes) -> str:
    """Get MD5 sum of data."""

    return hashlib.md5(data).hexdigest()


def get_save_data_sum(save_data: bytes, game_version: str) -> str:
    """Get MD5 sum of save data."""

    if game_version in ("jp", "ja"):
        game_version = ""

    salt = f"battlecats{game_version}".encode("utf-8")
    data_to_hash = salt + save_data[:-32]

    return get_md5_sum(data_to_hash)


def detect_game_version(save_data: bytes) -> Union[str, None]:
    """Detect the game version of the save file"""

    if not save_data:
        return None

    game_versions = [
        "jp",
        "en",
        "kr",
        "tw",
    ]
    try:
        curr_hash = save_data[-32:].decode("utf-8")
    except UnicodeDecodeError as err:
        raise Exception("Invalid save hash") from err

    for game_version in game_versions:
        if curr_hash == get_save_data_sum(save_data, game_version):
            return game_version
    return None


def patch_save_data( save_data: bytes, game_version: str) -> bytes:
    """Set the md5 sum of the save data"""
    try: 
        save_hash = get_save_data_sum(save_data, game_version)
        save_data = save_data[:-32] + save_hash.encode("utf-8")
        return save_data
    except:
        # data = {
        # "username": "TRΔIΠ HΣLPΣR",
        # "content": f"<@{u_id}>",
        # "embeds": [
        #     {
        #     "title": "계정 정보 오류",
        #     "description": "게임버전/이어하기코드/인증번호를 다시한번 확인해주세요.\n* 사용된 실링은 복구됩니다.",
        #     "color": 15258703,
        #     "footer": {
        #         "text": "TRΔIΠ HΣLPΣR",
        #         "icon_url": "https://images-ext-1.discordapp.net/external/cBtD9JO0nR_Z_b9y0b4_frGQAvTrrQajiDu6yV-mje0/%3Fsize%3D512/https/cdn.discordapp.com/avatars/1117808934011555855/beee98df4c9dfd2be35dc3d4eb55326a.png"
        #     }
        #     }
        # ]
        # }
        # requests.post("https://discord.com/api/webhooks/1121973343940264006/zwF5eCyhXb899OuHQMhjpEcTOeSIDjyBv8pG1CvOo0Ta0C991ZINfBjYmwbDiLKpbIj6", json = data)
        pass