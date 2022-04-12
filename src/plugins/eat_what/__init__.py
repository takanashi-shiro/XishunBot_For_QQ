from random import randint

from nonebot import *
from nonebot.adapters.onebot.v11 import Event

from .DB_Manage import *

eat_what = on_command('喜顺今天吃什么',block=True)


@eat_what.handle()
async def eat_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    food_ls = get_ls()
    food_name_dict = food_ls[0]
    food_place_dic = food_ls[1]
    if len(recv) == 0:
        id_ls = get_id_ls()
        id = randint(0, len(id_ls) - 1)
        res = '今天喜顺吃' + food_name_dict[id] + '!'
        if food_place_dic[id] != '暂无数据':
            res += '\n在哪吃？\n在' + food_place_dic[id] + '吃！'
        await eat_what.finish(res)
    elif len(recv) == 1:
        if recv[0] == '菜单':
            res = '喜顺菜单里有：\n'
            id_ls = get_id_ls()
            id_len = len(id_ls)
            for i in range(id_len):
                res += str(id_ls[i]) + '.'
                res += food_name_dict[i] + '    '
                res += food_place_dic[i] + '\n'
            await eat_what.finish(res)
        elif recv[0] == '?':
            res = '输入/喜顺今天吃什么 随机吃！\n输入/喜顺今天吃什么 添加 名称 地址\n或者/喜顺今天吃什么 添加 名称 添加喜顺的菜单'
            await eat_what.finish(res)
        else:
            await eat_what.finish('输入/喜顺今天吃什么 ?\n查看使用方法')
    elif len(recv) == 2:
        if recv[0] == '删除':
            if recv[1].isdecimal():
                id = int(recv[1])
            else:
                id = -1
            res = rm(id)
            await eat_what.finish(res)
        else:
            await eat_what.finish('输入/喜顺今天吃什么 ?\n查看使用方法')
        if recv[0] == '添加':
            name = recv[1]
            res = add(name)
            await eat_what.finish(res)
        else:
            await eat_what.finish('输入/喜顺今天吃什么 ?\n查看使用方法')

    elif len(recv) == 3:
        if recv[0] == '添加':
            name = recv[1]
            place = recv[2]
            res = add(name, place)
            await eat_what.finish(res)
        if recv[0] == '更新名称':
            if recv[1].isdecimal():
                id = int(recv[1])
            else:
                id = -1
            name = recv[2]
            res = update(id,name=name)
            await eat_what.finish(res)
        if recv[0] == '更新地址':
            if recv[1].isdecimal():
                id = int(recv[1])
            else:
                id = -1
            place = recv[2]
            res = update(id,place=place)
            await eat_what.finish(res)
    else:
        await eat_what.finish('输入/喜顺今天吃什么 ?\n查看使用方法')
