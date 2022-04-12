from time import strftime, localtime

from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageEvent, FriendAddNoticeEvent, RequestEvent, GroupRequestEvent, \
    FriendRequestEvent
import os
req = on_request()

@req.handle()
async def req_auto_approve(bot: Bot, event: RequestEvent):
    conv_s = {
        "user": [event.user_id] if isinstance(event, FriendRequestEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupRequestEvent) else [],
    }
    type = (
        event.sub_type if isinstance(event, GroupRequestEvent) else event.request_type
    )
    header = f"【请求】{event.flag}\n"
    sender = (await bot.get_stranger_info(user_id=event.user_id))[
                 "nickname"
             ] + f" {strftime('%Y-%m-%d %H:%M:%S', localtime(event.time))} \n"
    message = (
            ("邀请" if type == "invite" else "请求")
            + (
                "添加为好友"
                if type == "friend"
                else "加入群聊"
                     + (await bot.get_group_info(group_id=event.group_id))["group_name"]
                     + f" ({event.group_id})\n"
            )
            + (f"\n备注：{event.comment}" if event.comment else "")
    )
