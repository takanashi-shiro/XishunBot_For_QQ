import time

import nonebot
from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment

from .database.DB_Manage import *
from .elc.get_elc import get_elc_main, get_elc_main_second, get_elc

query = on_command('查电费',block=True)
scheduler_elc = require("nonebot_plugin_apscheduler").scheduler

@scheduler_elc.scheduled_job("cron", hour="0-23/4")
async def get_elc_every_4_hour():
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(t)
    msg = get_elc_main_second()
    bot = nonebot.get_bot()
    await bot.call_api('send_msg', message_type='private', user_id=764806602, message=msg)

@query.handle()
async def query_elc_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    qq_number = str(event.user_id)
    to_user(qq_number)
    print(recv)
    print(len(recv))
    if len(recv) == 3:
        if recv[0] == '绑定':
            building = recv[1]
            room = recv[2]
            dicts = get_elc(building,room)
            elc = dicts['resultData']['eledetail']
            msg = insert(qq_number,building,room,0)
            today_time = str(datetime.datetime.now()).split('.')[0]
            today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
            update_sys(qq_number, building, room, float(elc), today_time)
            msg += ser_by_qq(qq_number)
            await query.finish(msg)
    elif len(recv) == 2:
        building = recv[0]
        room = recv[1]
        if type(int(building)) == type(int(room)) == type(1):
            dicts = get_elc(building, room)
            elc = dicts['resultData']['eledetail']
            res = '寝室号：%s\n剩余电量: %s 度\n剩余金额: %s 元\n' % (
                room, '{:.2f}'.format(float(elc) / elc_unit_price), str(elc))
            await query.finish(res)
    elif len(recv) == 1:
        if recv[0] == '解除绑定':
            msg = unband(qq_number)
            await query.finish(msg)
        elif recv[0] == '更新':
            msg = get_elc_main_second()
            await bot.call_api('send_msg', message_type='private', user_id=764806602, message=msg)
    elif len(recv) == 0:
        msg = ser_by_qq(qq_number)

        await query.finish(msg)
    else:
        await query.finish("使用方法:\n输入/查电费 <栋> <房间号>查询当前剩余电费\n例如查询14栋612: /查电费 14 612\n输入/查电费 绑定 <栋> <房间号>以进行qq号与房间绑定\n输入/查电费 解除绑定 以对当前绑定的房间解绑\n")


