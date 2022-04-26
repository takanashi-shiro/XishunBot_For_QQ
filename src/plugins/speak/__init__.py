import nonebot.adapters.cqhttp
from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11 import Message
from .baidu import *

speak = on_message()

@speak.handle()
async def speak_main(bot: Bot, event: Event):
    res = baidu(str(event.get_message()))
    await speak.finish(res)
