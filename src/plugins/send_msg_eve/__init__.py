from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageEvent

import os
send_msg_eve = on_command('send_msg',block=True)

@send_msg_eve.handle()
async def send_msg_eve_main(bot: Bot, event: MessageEvent):
    recv = str(event.message)
    extra_msg = event.reply
    print(extra_msg)
    if extra_msg is None:
        extra_msg = ''
    else:
        extra_msg = str(extra_msg.message)
    print(extra_msg)
    recv_ls = recv.split()
    if len(recv_ls) >= 2:
        key_type_id = 'user_id'
        msg_type = 'private'
        if recv_ls[0] == '群聊':
            msg_type = 'group'
            key_type_id = 'group_id'
        send_id = int(recv_ls[1])
        msg = ''
        if len(recv_ls) >= 3:
            print(recv_ls[2:])
            for i in recv_ls[2:]:
                msg += i
        data = {
            'message_type':msg_type,
            key_type_id:send_id,
            'message':msg+extra_msg
        }
        print(data)
        msg = msg+extra_msg
        if msg_type == 'private':
            await bot.call_api('send_msg',message_type=msg_type,user_id=send_id,message=msg)
        else:
            await bot.call_api('send_msg',message_type=msg_type,group_id=send_id,message=msg)