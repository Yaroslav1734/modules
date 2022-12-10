# meta developer: @imalite, @CTOHKC (на основе его кода)
# requires: requests

import requests
from .. import loader, utils
from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


async def check(proxy: list):
    good = []
    bad = []
    for pro in proxy:
        try:
            requests.get("http://google.com", proxies={"http": f"http://{pro}"})
        except Exception as e:
            bad.append(pro)
        else:
            good.append(good)

    return [good, bad]


@loader.tds
class ProxyCheckerMod(loader.Module):
    """Module for checking proxies"""

    strings = {
        "name": "ProxyChecker",
        "no_proxy": "<b>Specify proxy in args!</b>",
        "results": ("<b>Good: </b><code>{}</code>" "\n<b>Bad: </b><code>{}</code>"),
    }

    strings_ru = {
        "no_proxy": "<b>🚫 Укажи прокси в аргументах!</b>",
        "results": (
            "<b>Рабочие: </b><code>{}</code>" "\n<b>Нерабочие: </b><code>{}</code>"
        ),
        "_cls_doc": "Модуль для проверки прокси",
        "_cmd_doc_checkproxy": "В аргументах укажи прокси",
    }

    def __init__(self) -> None:
        pass

    async def client_ready(self, client, db):
        pass

    async def checkproxycmd(self, message: Message):
        """Specify proxy in args"""

        args = utils.get_args(message)

        if not args:
            await utils.answer(message, self.strings["no_proxy"])
            return

        results = await check(args)
        await utils.answer(
            message, self.strings["results"].format(len(results[0]), len(results[1]))
        )
