from nonebot import *
from nonebot.adapters.onebot.v11 import Event

from .get_now_grade import get_now_grade
from .DB_Manage import *

codeforce = on_command('cf',block=True)


@codeforce.handle()
async def codeforce_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    qq_number = str(event.user_id)
    to_user(qq_number)
    if len(recv) == 1:
        if recv[0] == 'ls':
            dicts = get_ls()
            max_page = int(len(dicts) / 10) + 1
            cnt = 0
            msg = 'rank\n'
            for i in dicts:
                msg += i + ' : ' + str(dicts[i][0]) + '\n'
                cnt += 1
                if cnt == 10:
                    break
            msg += '第 1/%d 页' % max_page
            await codeforce.finish(msg)
        elif recv[0] == 'update':
            msg = update()
            await codeforce.finish(msg)
        else:
            await codeforce.finish("输入/cf ls查看当前列表所有人的分数\n" +
                                   "输入/cf add 用户名 进行添加用户\n" +
                                   "输入/cf del 用户名 进行删除用户\n" +
                                   "输入/cf ser 用户名 查看该用户分数")
    elif len(recv) == 2:
        if recv[0] == 'ls':
            if recv[1].isdecimal():
                page = int(recv[1])
            else:
                page = -1
            dicts = get_ls()
            max_page = int(len(dicts) / 10) + 1
            if not (page >= 1 and page <= max_page):
                await codeforce.finish("请输入正确页码")
            msg = 'rank\n'
            name_ls = list(dicts.keys())
            grade_ls = list(dicts.values())
            print(name_ls)
            print(grade_ls)
            length = 10
            if page == max_page:
                length = (len(dicts)-(max_page-1)*10)
            for i in range(0, length):
                msg += name_ls[(page-1)*10+i] + ' : ' + str(grade_ls[(page-1)*10+i][0]) + '\n'
            msg += '第 ' + str(page) + '/%d 页' % max_page
            await codeforce.finish(msg)
        if recv[0] == 'add':
            msg = add(qq_number, recv[1])
            await codeforce.finish(msg)
        elif recv[0] == 'del':
            msg = rm(recv[1])
            await codeforce.finish(msg)
        elif recv[0] == 'ser':
            msg = ''
            grade = ser(recv[1])
            msg += str(recv[1]) + '的当前分数为: ' + str(grade[0]) + '，最高分数为: ' + str(grade[1]) + '\n'
            await codeforce.finish(msg)
        else:
            await codeforce.finish("输入/cf ls查看当前列表所有人的分数\n" +
                                   "输入/cf add 用户名 进行添加用户\n" +
                                   "输入/cf del 用户名 进行删除用户\n" +
                                   "输入/cf ser 用户名 查看该用户分数")
    else:
        await codeforce.finish("输入/cf ls查看当前列表所有人的分数\n" +
                               "输入/cf add 用户名 进行添加用户\n" +
                               "输入/cf del 用户名 进行删除用户\n" +
                               "输入/cf ser 用户名 查看该用户分数")
