import base64
import time
import bs4
from nonebot import *
from nonebot.adapters.onebot.v11 import Event
from nonebot.typing import T_State
from nonebot.params import State

from .class_update_to_sql import get_simple_info
from .get_kb import get_kb
from .get_week import get_now_week
from .in_week import in_week
from .login import login
from .DB_Manage import *

query_kb = on_command('查课表',block=True)
query_score = on_command('查成绩',block=True)
qquser_dist = {
    '764806602': 'MTk0MDU2MjAwMDE=%%%bGtqaDQwMTAwMjc='
}
class_map = {
    'name': '课程',
    'content': '内容',
    'teacher': '教师',
    'class': '节次',
    'pos': '上课地点',
    'weeks': '上课周次',
    'week_flag': '单双周',
    'day': '星期'
}

trans = ['日', '一', '二', '三', '四', '五', '六', '日']


def get_scores(session):
    url = "http://218.75.197.123:83/jsxsd/dzqd/download_csnf?xsfs"
    res = url+'&JSESSIONID='+session.cookies.get("JSESSIONID")
    return res


def get_res(now_week,now_day,class_ls):
    res_ls=[]
    for i in class_ls:
        if in_week(now_week, i['weeks']) and now_day == i['day']:
            if i['week_flag'] == '单周' and eval(now_week) % 2 == 1:
                res_ls.append(i)
            elif i['week_flag'] == '双周' and eval(now_week) % 2 == 0:
                res_ls.append(i)
            elif i['week_flag'] == '每周':
                res_ls.append(i)
    res = "课表:\n"
    print(res_ls)
    if len(res_ls) == 0:
        return '开心嘛，没课哦！'
    for i in res_ls:
        for keys in i:
            res += class_map[keys] + " : " + i[keys].strip() + "\n"
        res += "========\n"
    return res


@query_score.handle()
async def query_score_main(bot: Bot, event: Event, state: T_State = State()):
    qq_number = event.get_user_id()
    if qq_number in qquser_dist.keys():
        encode = qquser_dist[str(event.get_user_id())]
        sessions = login(encode)
        res = get_scores(sessions)
        await bot.call_api('send_msg',message_type='private',user_id=qq_number,message=res)
        await query_score.finish('查询成功了！快去康康私聊！')
    else:
        await query_score.finish('暂无信息，快去用查课表绑定一下腻')
    pass

@query_kb.handle()
async def query_kb_main(bot: Bot, event: Event, state: T_State = State()):
    global qquser_dist
    qquser_dist = get_ls()
    recv = str(event.message).split()
    recv.pop(0)
    if not recv:
        if event.get_user_id() in qquser_dist.keys():
            encode = qquser_dist[str(event.get_user_id())]
            sessions = login(encode)
            now_week = get_now_week(sessions)
            class_ls = get_kb(sessions)
            nowtime = time.localtime()
            nowday = str(time.strftime("%w", nowtime))
            await query_kb.send("现在是第" + now_week + "周,星期" + trans[eval(nowday)] + "\n")
            res_tmp = get_res(now_week, nowday, class_ls)
            if res_tmp != '开心嘛，没课哦！':
                res = '本日' + res_tmp
            else:
                res = res_tmp
            await query_kb.finish(res)
        else:
            await query_kb.finish("未绑定学生账号\n输入/查课表 绑定 <账号> <密码> 即可绑定\n例如/查课表 绑定 123 123\n查询用法请输入\n/查课表 ?\n")
    elif len(recv) == 3:
        if str(recv[0]) == '绑定':
            username_tmp = recv[1]
            passwd_tmp = recv[2]
            encode_username = base64.b64encode(username_tmp.encode("utf-8")).decode('utf-8')
            encode_passwd = base64.b64encode(passwd_tmp.encode("utf-8")).decode('utf-8')
            qq_id = str(event.get_user_id())
            encode = encode_username + "%%%" + encode_passwd
            if not is_qq_exist(qq_id):
                res = update(qq_id, encode)
            else:
                res = qq_to_cookie(qq_id, encode)
            qquser_dist = get_ls()
            await query_kb.finish(res)
        elif str(recv[0]) == '查':
            if event.get_user_id() in qquser_dist.keys():
                encode = qquser_dist[str(event.get_user_id())]
                sessions = login(encode)
                class_ls = get_kb(sessions)
                week = str(recv[1])
                day = str(recv[2])
                if day == '7':
                    day = '0'
                res = get_res(week, day, class_ls)
                await query_kb.finish(res)
            else:
                await query_kb.finish("未绑定学生账号\n输入/查课表 绑定 <账号> <密码> 即可绑定\n例如/查课表 绑定 123 123")
    elif len(recv) == 1:
        if recv[0] == "?":
            await query_kb.finish("使用方法：\n1. /查课表 绑定 <账号> <密码>\n绑定教务系统账号(不带<>)\n" +
                                  "2. /查课表\n查询当天课表\n" +
                                  "3. /查课表 查 <周次> <星期几>\n查询指定日期课表(不带<>，输数字)，例如查第三周星期五课表\n/查课表 查 3 5\n" +
                                  "本系统仅用于查课表，信息用于获取cookies，该系统仅存储cookies")
        elif recv[0] == "解除绑定":
            qq_id = str(event.get_user_id())
            qquser_dist.pop(qq_id)
            await query_kb.finish("解除绑定成功，数据已删除")
        elif recv[0] == "明天":
            if event.get_user_id() in qquser_dist.keys():
                encode = qquser_dist[str(event.get_user_id())]
                sessions = login(encode)
                class_ls = get_kb(sessions)
                week = get_now_week(sessions)
                nowtime = time.localtime()
                day = int(time.strftime("%w", nowtime))
                if day == 0:
                    week = str(int(week)+1)
                    day = str(1)
                else:
                    day = str((day+1) % 7)
                res_tmp = get_res(week, day, class_ls)
                if res_tmp != '开心嘛，没课哦！':
                    res = '明日' + res_tmp
                else:
                    res = res_tmp
                await query_kb.finish(res)
            else:
                await query_kb.finish("未绑定学生账号\n输入/查课表 绑定 <账号> <密码> 即可绑定\n例如/查课表 绑定 123 123")
