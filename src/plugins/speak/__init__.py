import nonebot.adapters.cqhttp
from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11 import Message
from .baidu import *
from .translate import translate
from .DB_Manage import get_status
speak = on_message(priority=5)

@speak.handle()
async def speak_main(bot: Bot, event: Event):
    msg = str(event.get_message())
    res = baidu(msg)
    qq_number = str(event.user_id)
    if res != None:
        await speak.finish(res)
    elif get_status(qq_number):
        res = translate(msg)
        await speak.finish(res)
