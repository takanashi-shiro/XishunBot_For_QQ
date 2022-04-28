# -*- coding: utf-8 -*-

from nonebot import on_command
from nonebot.rule import regex, to_me
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State

from .gacha import *
from nonebot.params import State
arknights = on_command("抽卡", rule=regex(r"\w{1,2}$"),block=True)
# regex(r"\d{1,2}$")

@arknights.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State = State()):
    args = str(event.message).split()  # 首次发送命令时跟随的参数 1, 10
    args.pop(0)
    if args:
        state["roll_times"] = str(args[0])  # 如果用户发送了参数则直接赋值


@arknights.got("roll_times", prompt="单抽输入1, 十连输入10")
async def handle_roll_times(bot: Bot, event: Event, state: T_State = State()):
    roll_times = str(state["roll_times"])
    # 在这里对参数进行验证
    if str(state["roll_times"]) not in ["1", "10"]:
        await arknights.finish("不支持自定义次数抽卡")

    result_list = arknights_gacha(int(roll_times))
    await arknights.finish(result_list)
