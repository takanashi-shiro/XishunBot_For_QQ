from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment

from .yiyan import yiyan

one_speak = on_command('yy')

@one_speak.handle()
async def _test(bot: Bot, event: Event):
    await one_speak.finish(yiyan())
