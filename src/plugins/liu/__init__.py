from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment, Message
from .liu2 import liu2
from .dao import dao_work

liu = on_command('溜',block=True)


@liu.handle()
async def liu_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    if len(recv) == 1 and recv[0] == '?':
        name_ls = liu2()[3]
        res = '当前歌单：\n'
        cnt = 1
        for i in name_ls:
            tmp = str(cnt) + '. ' + i + ';\n'
            res += tmp
            cnt += 1
        msg = MessageSegment.text(res)
        await liu.send(msg)
        msgs = '[/溜]随机溜\n[/溜 ?]显示歌单及教程\n[/溜 序号]如/溜 1'
        msg = MessageSegment.text(msgs)
        await liu.finish(msg)
    elif len(recv) == 1:
        if recv[0].isdecimal():
            numb = int(recv[0])
        else:
            numb = -1
        music_ls = liu2()[2]
        name_ls = liu2()[3]
        msgs = "请欣赏金曲：" + name_ls[numb - 1]
        msg = MessageSegment.text(msgs)
        await liu.send(msg)
        msgs = music_ls[numb - 1]
        msg = MessageSegment.record(file=msgs)
        await liu.finish(msg)
    elif (len(recv) == 2 or len(recv) == 3) and recv[0] == 'add':
        url = recv[1]
        bv = url[url.find('BV') + 2:]
        p = '1'
        if len(recv) == 3:
            p = recv[2]
        msgs = dao_work(bv, p)
        print(msgs)
        await liu.send(msgs[1])
        await liu.finish(
            # MessageSegment.record(file=msgs[2].replace(r'\\', '/'))
            Message(f'[CQ:record,file=file:///' + msgs[2] + ']')
        )

    else:
        tmp = liu2()
        msgs = str(tmp[0])
        msg = MessageSegment.text(msgs)
        await liu.send(msg)
        msgs = tmp[1]
        msg = MessageSegment.record(file=msgs)
        await liu.finish(msg)
