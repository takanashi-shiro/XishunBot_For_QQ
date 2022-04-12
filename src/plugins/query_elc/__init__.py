from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from .choose_building import choose_building
from .choose_room import choose_room
from .query_elc import query_elc
from .DB_Manage import *

query = on_command('查电费',block=True)


@query.handle()
async def query_elc_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    qq_number = str(event.user_id)
    to_user(qq_number)
    print(recv)
    print(len(recv))
    if len(recv) == 2:
        if recv[0].isdecimal():
            building = int(recv[0]) - 1
        else:
            building = -1
        building_name = choose_building()[0][building]
        building_id = choose_building()[1][building]
        room = recv[1]
        search = str(choose_building()[1][building])
        room_id = str(choose_room(search)[1][choose_room(search)[0].index(room)])
        res = query_elc(room_id)[0]
        await query.finish(res)
    elif len(recv) == 3 and recv[0] == '绑定':
        building = recv[1]
        room = recv[2]
        msg = insert(qq_number,building,room)
        await query.finish(msg)
    elif len(recv) == 1:
        if recv[0] == '解除绑定':
            msg = unband(qq_number)
            await query.finish(msg)
    elif len(recv) == 0:
        msg = ser_by_qq(qq_number)
        await query.finish(msg)
    else:
        await query.finish("使用方法:\n输入/查电费 <栋> <房间号>查询当前剩余电费\n例如查询14栋612: /查电费 14 612\n输入/查电费 绑定 <栋> <房间号>以进行qq号与房间绑定\n输入/查电费 解除绑定 以对当前绑定的房间解绑\n")


