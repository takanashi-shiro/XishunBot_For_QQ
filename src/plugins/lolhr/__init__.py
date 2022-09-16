# import nonebot.adapters.cqhttp
from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment

lolhr = on_command('lolhr')
member_list = {
    '853153131': ['764806602']
}


@lolhr.handle()
async def _test(bot: Bot, event: Event):

    group_num = str(event.group_id)
    if group_num not in member_list.keys():
        member_list[group_num] = ['764806602']
    recv = str(event.message).strip()
    recv.pop(0)
    if recv:
        if recv == '?':
            await lolhr.finish("使用方法：\n发送/lolhr<空格>{你的qq号} 即可绑定该群lol一键喊人\n发送/lolhr<空格>rm<空格>{QQ号}删除本群喊人列表内成员\n发送/lolhr<空格>show展示喊人列表")
        recv_list = recv.split()
        if "rm" in recv_list:
            recv = recv_list[1]
            recv = eval(recv)
            recv = str(recv)
            member_list[group_num].remove(recv)
            await lolhr.finish("删除"+recv+"成功")
        elif "show" in recv_list:
            qq_list = member_list[group_num]
            msgs = [MessageSegment.text("喊人列表:\n")]
            for qqid in qq_list:
                qqid=qqid+"\n"
                msgs.append(MessageSegment.text(qqid))

            await lolhr.finish(message=msgs)
        else:
            recv = eval(recv)
            recv = str(recv)
            member_list[group_num].append(recv)
            await lolhr.finish("保存成功")
    else:
        qq_list = member_list[group_num]
        msgs = []
        for qqid in qq_list:
            msgs.append(MessageSegment.at(user_id=qqid))
        await lolhr.finish(message=msgs)
