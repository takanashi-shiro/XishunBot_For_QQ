from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageEvent

def get_groups_id(bot:Bot):
    ids = [group["group_id"] for group in (await bot.get_group_list())]
    print(ids)
