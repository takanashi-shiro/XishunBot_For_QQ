from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment

menu = on_command('?')

@menu.handle()
async def _menu_list(bot: Bot, event: Event):
    menu_list = [
        '喜顺bot功能列表',
        '1. "/lolhr" 一键喊人',
        '2. "/溜"     随机溜',
        '3. "/xishun" 开摆',
        '4. "/yy"     每日一言',
        '6. "/?"      功能菜单',
        '7. "/查电费"  查电费',
        '8. "/查课表"  查课表',
        '9. "/cf"     codeforces分数查询'
    ]
    msg = ''
    for i in menu_list:
        msg += i + '\n'
    msg = msg.strip('\n')
    await menu.finish(msg)
