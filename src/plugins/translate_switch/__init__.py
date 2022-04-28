from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from .DB_Manage import *
trans_switch = on_command('翻译',block=True)

@trans_switch.handle()
async def trans_switch_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    qq_number = str(event.user_id)
    to_user(qq_number)
    if len(recv) == 1:
        res = '出错'
        if recv[0] == '开':
            res = update(qq_number,1)
        if recv[0] == '关':
            res = update(qq_number,0)
        await trans_switch.finish(res)
    elif len(recv) == 0:
        status = get_status(qq_number)
        res = '出错'
        if status:
            res = update(qq_number,0)
        else:
            res = update(qq_number,1)
        await trans_switch.finish(res)


