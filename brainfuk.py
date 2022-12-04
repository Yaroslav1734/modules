# meta developer: @imalite
# meta desc: Интерпретатор Brainfuck в виде модуля, не поддерживается оператор ,


from .. import loader, utils
from telethon.tl.types import Message
from ..inline.types import InlineQuery


def loops(code):
    opened = []
    blocks = {}
    for i in range(len(code)):
        if code[i] == "[":
            opened.append(i)
        elif code[i] == "]":
            blocks[i] = opened[-1]
            blocks[opened.pop()] = i
    return blocks


def run(code):
    code = "".join(c for c in code if c in "><+-.[]")
    res = ""
    x = i = 0
    bf = {0: 0}
    blocks = loops(code)
    l = len(code)
    while i < l:
        sym = code[i]
        if sym == ">":
            x += 1
            bf.setdefault(x, 0)
        elif sym == "<":
            x -= 1
        elif sym == "+":
            bf[x] += 1
        elif sym == "-":
            bf[x] -= 1
        elif sym == ".":
            res + chr(bf[x])
        elif sym == "[":
            if not bf[x]:
                i = blocks[i]
        elif sym == "]":
            if bf[x]:
                i = blocks[i]
        i += 1
    return res


class Brainfuk(loader.Module):
    """Интерпретатор Brainfuck в виде модуля, не поддерживается оператор ,"""

    def __init__(self, *_) -> None:
        pass

    strings = {
        "name": "Brainfuck",
        "result": "<b>📼 Code: </b><code>{}</code>\n<b>🔮 Result: </b><code>{}</code>",
        "no_args": "<b>🚫 Specify args!</b>",
    }

    strings_ru = {
        "result": "<b>📼 Код: </b><code>{}</code>\n<b>🔮 Результат: </b><code>{}</code>",
        "no_args": "<b>🚫 Укажи аргументы!</b>",
    }

    async def brainfuckcmd(self, message: Message):
        """В аргументах нужно указать код brainfuck"""
        try:
            args = utils.get_args(message)[0]
        except:
            await utils.answer(message, self.strings["no_args"])
            return

        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            result = run(args)
        except:
            result = None

        if result == "":
            result = "No result"

        await utils.answer(message, self.strings["result"].format(args, result))

