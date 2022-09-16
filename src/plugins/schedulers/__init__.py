import time

from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.typing import T_State
from nonebot.params import State

from .wmxy.database.mysql_data import insert_stu, exist_qq, update_stu
from .wmxy.login.campus import login_by_SMS
from .wmxy.login.login import qq_bot_run

scheduler = require("nonebot_plugin_apscheduler").scheduler
wmxy_register = on_command('完美校园注册', block=True)
wmxy_band = on_command('完美校园绑定', block=True)
wmxy_daka = on_command('健康打卡', block=True)


@scheduler.scheduled_job("cron", hour="3-12/6")
async def run_every_8_hour():
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{}'.format(t))
    qq_bot_run()


@wmxy_register.handle()
@wmxy_band.handle()
async def wmxy_First(bot: Bot, event: Event, state: T_State = State()):
    state["qq_number"] = str(event.user_id)
    args = str(event.message).split()
    args.pop(0)
    if args:
        state["phone"] = str(args[0])  # 如果用户发送了参数则直接赋值


@wmxy_register.got("phone", prompt="输入手机号")
async def wmxy_login_Second(bot: Bot, event: Event, state: T_State = State()):
    phone = str(state["phone"])
    if phone.isalnum() and len(phone) == 11:
        t = login_by_SMS(phone, phone)
        t.sendSMS()
        state["SMS_Session"] = t
        await wmxy_register.send("短信已发送")
    else:
        await wmxy_register.finish("发送失败")


@wmxy_band.got("phone", prompt="输入手机号")
async def wmxy_band_Second(bot: Bot, event: Event, state: T_State = State()):
    phone = str(state["phone"])
    if phone.isalnum() and len(phone) == 11:
        await wmxy_band.send("您的手机号为" + phone)
    else:
        await wmxy_band.finish("请输入正确的手机号")


@wmxy_band.got("passwd", prompt="输入密码")
async def wmxy_band_Third(bot: Bot, event: Event, state: T_State = State()):
    passwd = str(state["passwd"])
    await wmxy_band.send("您的密码为" + passwd)
    qq_number = state["qq_number"]
    phone = state["phone"]
    if exist_qq(qq_number):
        ans = update_stu(qq_number=qq_number, phone=phone, passwd=passwd)
    else:
        ans = insert_stu(qq_number=qq_number, phone=phone, wmxy_passwd=passwd)
    await wmxy_band.finish(ans)


@wmxy_register.got("passwd", prompt="输入密码")
async def wmxy_band_Third(bot: Bot, event: Event, state: T_State = State()):
    passwd = str(state["passwd"])
    await wmxy_register.send("您的密码为" + passwd)
    qq_number = state["qq_number"]
    phone = state["phone"]
    if exist_qq(qq_number):
        ans = update_stu(qq_number=qq_number, phone=phone, passwd=passwd)
    else:
        ans = insert_stu(qq_number=qq_number, phone=phone, wmxy_passwd=passwd)
    await wmxy_register.send(ans)


@wmxy_register.got("SMS_code", prompt="输入验证码")
async def wmxy_login_Finnal(bot: Bot, event: Event, state: T_State = State()):
    SMS_code = str(state["SMS_code"])
    passwd = str(state["passwd"])
    phone = state["phone"]
    await wmxy_register.send("验证码为" + SMS_code)
    t = state["SMS_Session"]
    ans = t.authSMS(SMS_code)
    qq_number = state["qq_number"]
    if ans == '登入成功':
        if exist_qq(qq_number):
            update_stu(qq_number, phone, passwd)
    await wmxy_register.send(
        ans + "\n您的设备id是" + str(t.user_info['deviceId']) + "\n" + "请不要使用完美校园app，否则会挤掉这里的用户，如果挤掉了需要来重新绑定。")


@wmxy_daka.handle()
async def wmxy_daka_main(bot: Bot, event: Event):
    if str(event.user_id) == '764806602':
        qq_bot_run()
