# 
#                 █░░ █ ▀█▀ █▀▀
#                 █▄▄ █ ░█░ ██▄
# 
#               © Copyright 2023
# 
#          Licensed under the GNU GPLv3
#      https://www.gnu.org/licenses/agpl-3.0.html

# requires: aiohttp

import aiohttp
from telethon.tl.types import Message
from .. import loader, utils
from ast import literal_eval
from ..inline.types import InlineCall # type: ignore


async def generate_mail():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox") as request:
            return literal_eval(await request.text())[0]


async def get_messages(login: str, domain: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}") as request:
            if await request.text() == "[]":
                return None
            else:
                return literal_eval(await request.text())


async def read_message(login: str, domain: str, id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}") as request:
            if await request.text() == "Message not found":
                return None
            else:
                return literal_eval(await request.text())
    

async def is_valid_email(email: str):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.1secmail.com/api/v1/?action=getDomainList") as request:
            if len(email.split("@")) != 2:
                return False
            elif email.split("@")[1] not in await request.text():
                return False
            else:
                return True


@loader.tds
class TempMail(loader.Module):
    """Redesign of ftg module by @blazeftg. Generate temp mail and receive messages"""

    strings = {
        "name": "TempMail",
        "your_mail": (
            "<b><emoji document_id=5472107610087889157>📭</emoji>"
            " Your mail is created!<b>"
            "\n<code>{}</code>"
        ),
        "no_args": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Specify arguments!</b>"
        ),
        "message": (
            "<b><emoji document_id=5406631276042002796>📨</emoji>"
            " Message №{} (id {})</b>"
            "\n<b>🙍‍♂️ Sender: {}</b>"
            "\n"
            "<b><emoji document_id=5420315771991497307>🔥</emoji> Subject: {}</b>"
            "\n"
            "<b><emoji document_id=5451732530048802485>⏳</emoji> Time: </b><code>{}</code>"
            "\n"
            "<b><emoji document_id=5472319622558522557>📝</emoji> Text: </b><code>{}</code>"
        ),
        "messages": (
            "<b>✉ All messages</b>"
        ),
        "back": (
            "🔙 Back"
        )
    }

    strings_ru = {
        "your_mail": (
            "<b><emoji document_id=5472107610087889157>📭</emoji>"
            " Твоя почта создана!<b>"
            "\n<code>{}</code>"
        ),
        "no_args": (
            "<b><emoji document_id=5465665476971471368>❌</emoji>"
            " Укажи аргументы!</b>"
        ),
        "no_messages": (
            "<b><emoji document_id=5424885441100782420>👀</emoji>"
            " Mail empty</b>"
        ),

        "message": (
            "<b><emoji document_id=5406631276042002796>📨</emoji>"
            " Сообщение №{} (айди {})</b>"
            "\n<b>🙍‍♂️ Отправитель: {}</b>"
            "\n"
            "<b><emoji document_id=5420315771991497307>🔥</emoji> Тема: {}</b>"
            "\n"
            "<b><emoji document_id=5451732530048802485>⏳</emoji> Время: </b><code>{}</code>" 
            "\n"
            "<b><emoji document_id=5472319622558522557>📝</emoji> Текст: </b><code>{}</code>"
        ),
        "messages": (
            "<b>✉ Все сообщения</b>"
        ),
        "no_messages": (
            "<b><emoji document_id=5424885441100782420>👀</emoji>"
            " Почта пустая</b>"
        ),
        "back": (
            "🔙 Назад"
        ),
        "_cls_doc": (
            "Переработка модуля для FTG от @blazeftg. Генерация временной почты и получение писем."
        )
    }


    def __init__(self) -> None:
        pass

    async def client_ready(self):
        pass


    @loader.command(
        ru_doc = "Генерация временной почты"
    )
    async def tempmail(self, message: Message):
        """Generate temp mail"""
        generated = await generate_mail()
        await utils.answer(
            message,
            self.strings["your_mail"].format(generated)
        )
    
    @loader.command(
        ru_doc = ".mailmsg <почта> - Получить все сообщения на почте"
    )
    async def mailmsg(self, message: Message):
        """.mailmsg <mail> - Get all messages on mail"""

        args = utils.get_args_raw(message)
        if not args or not await is_valid_email(args):
            await utils.answer(
                message,
                self.strings["no_args"]
            )
            return
        
        messages = await get_messages(args.split("@")[0], args.split("@")[1])
        if messages == None:
            await utils.answer(
                message,
                self.strings["no_messages"]
            )
        else:
            reply_markup = []
            for i in range(len(messages)):
                reply_markup.append(
                    [
                        {
                            "text": f"№{i+1}",
                            "callback": self.msg_info,
                            "args": [messages, i, args.split("@")[0], args.split("@")[1]]
                        }
                    ]
                )
            
            await self.inline.form(
                text=self.strings["messages"],
                message=message,
                reply_markup=reply_markup,
                silent=True
            )
    
    async def msg_info(self, call: InlineCall, messages, i, login, domain):
        read = await read_message(login, domain, messages[i]["id"])
        await call.edit(
            self.strings["message"].format(
                i + 1,
                messages[i]["id"],
                utils.escape_html(messages[i]["from"]),
                utils.escape_html(messages[i]["subject"]),
                utils.escape_html(messages[i]["date"]),
                utils.escape_html(read["textBody"])
            ),
            reply_markup = [
                {
                    "text": self.strings["back"],
                    "callback": self.messages_,
                    "args": [messages, login, domain]
                }
            ]
        )
    
    async def messages_(self, call: InlineCall, messages, login, domain):

    
        reply_markup = []
        for i in range(len(messages)):
            reply_markup.append(
                [
                    {
                        "text": f"№{i+1}",
                        "callback": self.msg_info,
                        "args": [messages, i, login, domain]
                    }
                ]
            )
        
        await call.edit(
            self.strings["messages"],
            reply_markup=reply_markup,
        )
        
    