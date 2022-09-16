from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment

menu = on_command('菜单')

@menu.handle()
async def _menu_list(bot: Bot, event: Event):
    menu_list = [
        '喜顺bot功能列表',
        '1. "/lolhr" 一键喊人',
        '2. "/溜"     随机溜',
        '3. "/xishun" 开摆',
        '4. "/yy"     每日一言',
        '6. "/菜单"      功能菜单',
        '7. "/查电费"  查电费',
        '8. "/查课表"  查课表',
        '9. "/cf"     codeforces分数查询',
        '10. "/查天气"  查询天气',
        '11. "/查疫情"  查疫情情况',
        '12. /抽卡      模拟明日方舟抽卡',
        '13. /完美校园注册    登入完美校园',
        '14. /点歌   点一首歌儿来听'
    ]
    msg = ''
    for i in menu_list:
        msg += i + '\n'
    msg = msg.strip('\n')
    await menu.finish(msg)
