from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageEvent
import time
import random
announce_com = on_command('announce',block=True)

@announce_com.handle()
async def announce_main(bot: Bot, event: MessageEvent):
    group_ids = [group["group_id"] for group in (await bot.get_group_list())]
    user_ids =  [user["user_id"] for user in (await bot.get_friend_list())]
    user_nicknames = [user["nickname"] for user in (await bot.get_friend_list())]
    print("group_ids:"+str(group_ids))
    print("user_ids:"+str(user_ids))
    recv = str(event.message)
    extra_msg = event.reply
    print(extra_msg)
    if extra_msg is None:
        extra_msg = ''
    else:
        extra_msg = str(extra_msg.message)
    print(extra_msg)
    recv_ls = recv.split()
    if len(recv_ls) >= 1:
        key_type_id = 'user_id'
        msg_type = 'private'
        send_ids = user_ids
        if recv_ls[0] == '群':
            msg_type = 'group'
            key_type_id = 'group_id'
            send_ids = group_ids
        msg = ''
        if len(recv_ls) >= 2:
            print(recv_ls[1:])
            for i in recv_ls[1:]:
                msg += i
        cnt = 0
        for send_id in send_ids:
            data = {
                'message_type': msg_type,
                key_type_id: send_id,
                'message': msg + extra_msg
            }
            print(data)
            msg = msg + extra_msg
            times = random.uniform(0.7,3.4)
            time.sleep(times)
            if msg_type == 'private':
                await announce_com.send("用户："+user_nicknames[cnt]+" "+str(send_id)+"已发送\n目前进度"+"%d/%d"%(cnt+1,len(send_ids)))
                await bot.call_api('send_msg', message_type=msg_type, user_id=send_id, message=msg)
            else:
                await announce_com.send("群组:"+str(send_id) + "已发送\n目前进度"+"%d/%d"%(cnt+1,len(send_ids))")
                await bot.call_api('send_msg', message_type=msg_type, group_id=send_id, message=msg)
            cnt+=1