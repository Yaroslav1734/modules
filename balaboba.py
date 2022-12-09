# meta developer: @imalite, @CTOHKC

import requests, json
import urllib.request
from .. import loader, utils
from telethon.tl.types import Message


async def balabob(text):
    link = "https://yandex.ru/lab/api/yalm/text3"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://yandex.com",
        "Referer": "https://yandex.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx 05)",
        "sec-ch-ua": '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }
    data = {"query": f"{text}", "intro": 0, "filter": 1}
    params = json.dumps(data).encode("utf8")
    req = urllib.request.Request(link, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    res = response.read().decode("utf8")
    result = json.loads(res)
    return result["text"]


@loader.tds
class BalabobaMod(loader.Module):
    """Module for work with balaboba. Based on @balaboby_bot"""

    strings = {
        "name": "Balaboba",
        "work": "<b>😰 Wait...</b>",
        "no_args": "<b>🚫 Provide arguments!</b>",
    }

    strings_ru = {
        "work": "<b>😰 Ждем...</b>",
        "no_args": "<b>🚫 Укажи аргументы!</b>",
        "_cmd_doc_balaboba": "В аргументах укажи текст",
        "_cls_doc": "Модуль для работы с балабобой. Основан на @balaboby_bot",
    }

    async def client_ready(self, client, db):
        pass

    def __init__(self) -> None:
        pass

    async def balabobacmd(self, message: Message):
        """Specify text in args"""

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        await utils.answer(message, self.strings["work"])
        balaboba = await balabob(args)
        await utils.answer(message, "<b>{} </b><code>{}</code>".format(args, balaboba))
