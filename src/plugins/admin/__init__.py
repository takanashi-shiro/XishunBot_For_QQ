from nonebot import *
from nonebot.adapters.onebot.v11 import Event
import os
admin = on_command('admin',block=True)

@admin.handle()
async def admin_main(bot: Bot, event: Event):
    recv = str(event.message)
    try:
        rs = os.popen(recv)
        msg = rs.read()
        await admin.send(recv)
        await admin.finish(msg)
    except:
        await admin.finish('wa')


