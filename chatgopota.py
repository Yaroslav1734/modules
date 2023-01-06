# 
#                 █░░ █ ▀█▀ █▀▀
#                 █▄▄ █ ░█░ ██▄
# 
#               © Copyright 2023
# 
#          Licensed under the GNU GPLv3
#      https://www.gnu.org/licenses/agpl-3.0.html

# requires: chatgptpy
# meta developer: @imalite
# meta desc: Module for chatting with ChatGPT


import logging
import re
from pychatgpt import Chat
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ChatGoPoTaMod(loader.Module):
    """Module for chatting with ChatGPT"""

    strings = {
        "name": "ChatGoPoTa",
        "no_args": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Specify arguments!</b>"
        ),
        "error": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            "  There was an error"
            ", maybe you specified the wrong email and password"
            ", or maybe OpenAI is not supported in your country.</b>"
        ),
        "chat": (
            "<b><emoji document_id=5305794398938735107>💭</emoji>"
            " Your question: </b>{}"
            "\n<b><emoji document_id=5372981976804366741>🤖</emoji> ChatGPT answer: </b>{}"
        ),
        "no_email": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " You didn't specified email!</b>"
        ),
        "email_not_valid": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Email that you specified is not valid!</b>"
        ),
        "no_password": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " You didn't specified password!</b>"
        ),
        "password_not_valid": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Password that you specified is not valid!</b>"
        ),
        "email_set": (
            "<b><emoji document_id=5188216731453103384>✔️</emoji>"
            " Email is set!<b>"
        ),
        "password_set": (
            "<b><emoji document_id=5188216731453103384>✔️</emoji>"
            " Password is set!<b>"
        )
    }

    strings_ru = {
        "no_args": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Укажи аргументы!</b>"
        ),
        "error": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            "  Произошла ошибка"
            ", возможно ты указал неверные пароль и почту"
            ", или может OpenAI не поддерживается в твоей стране.</b>"
        ),
        "chat": (
            "<b><emoji document_id=5305794398938735107>💭</emoji>"
            " Твой вопрос: </b>{}"
            "\n<b><emoji document_id=5372981976804366741>🤖</emoji> Ответ ChatGPT: </b>{}"
        ),
        "no_email": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Ты не указал почту!</b>"
        ),
        "email_not_valid": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Почта которую ты указал неверная!</b>"
        ),
        "no_password": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Ты не указал пароль!</b>"
        ),
        "password_not_valid": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Пароль который ты указал неверный!</b>"
        ),
        "email_set": (
            "<b><emoji document_id=5188216731453103384>✔️</emoji>"
            " Почта установлена!<b>"
        ),
        "password_set": (
            "<b><emoji document_id=5188216731453103384>✔️</emoji>"
            " Пароль установлен!<b>"
        )
    }

    def __init__(self) -> None:
        ...
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(
        ru_doc = "<вопрос> - Начать переписку с ChatGPT"
    )
    async def chatgpt(self, message: Message):
        """<question> - Start conversation with ChatGPT"""

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(
                message,
                self.strings["no_args"]
            )
            return
        
        try:
            chat = Chat(self.get("email", ""), self.get("password", ""))
        except:
            await utils.answer(
                message,
                self.strings["error"]
            )
            return
        
        answer, _, _ = chat.ask(args)
        await utils.answer(
            message,
            self.strings["chat"].format(
                utils.escape_html(args),
                utils.escape_html(answer)
            )
        )
    
    @loader.command(
        ru_doc = "<email> - Установить email аккаунта OpenAI"
    )
    async def email(self, message: Message):
        """<email> - Set OpenAI account email"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                self.strings["no_email"]
            )
            return
        
        if not re.match(r"^\S+@\S+\.\S+$", args):
            await utils.answer(
                message,
                self.strings["email_not_valid"]
            )
            return
        
        self.set("email", args)
        await utils.answer(
            message,
            self.strings["email_set"]
        )

    @loader.command(
        ru_doc = "<password> - Установить пароль аккаунта OpenAI"
    )
    async def password(self, message: Message):
        """<password> - Set OpenAI account password"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                self.strings["no_password"]
            )
        if len(args) < 5:
            await utils.answer(
                message,
                self.strings["password_not_valid"]
            )
            return
        
        cyrillic = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        is_cyrillic = cyrillic.intersection(args.lower()) != set()
        if is_cyrillic: # cyrillic symbols in openai password is not allowed
            await utils.answer(
                message,
                self.strings["password_not_valid"]
            )
            return
        
        self.set("password", args)
        await utils.answer(
            message,
            self.strings["password_set"]
        )