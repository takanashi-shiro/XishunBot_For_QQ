import random
from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment

from .xishun import xishun

one_speak = on_command('xishun')


@one_speak.handle()
async def _test(bot: Bot, event: Event, ):
    ls_txt = xishun()[0]
    ls_amr = xishun()[1]
    a = random.randint(1, 100)
    txt = ls_txt[a%3]
    amr = ls_amr[a%3]
    await one_speak.send(txt)
    msg = MessageSegment.record(file=amr)
    await one_speak.finish(message=msg)
