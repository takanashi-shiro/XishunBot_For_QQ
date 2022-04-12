from nonebot import *
from nonebot.adapters.onebot.v11 import Event, MessageSegment, Message
from .get_weather import get_datas
from .DB_Manage import *
import time

ser_weather = on_command('查天气',block=True)

@ser_weather.handle()
async def weather_main(bot: Bot, event: Event):
    recv = str(event.message).split()
    recv.pop(0)
    qq_number = str(event.user_id)
    to_user(qq_number)
    if len(recv) == 1:
        if recv[0] != '?':
            if recv[0] == '解绑':
                res = unband(qq_number)
                await ser_weather.finish(res)
            else:
                city = get_city(qq_number)
                if not get_city(qq_number):
                    await ser_weather.finish(city)

                now_temperature, yesterday_data, forecast_datas = get_datas(city)
                yes_res = '昨天是%s，%s\n%s\n%s\n风向：%s' % \
                          (
                          yesterday_data['date'], yesterday_data['type'], yesterday_data['low'], yesterday_data['high'],
                          yesterday_data['fx'])
                now_next_5_days_res = []
                for datas in forecast_datas:
                    tmp_res = '%s，%s\n%s\n%s\n风向：%s' % \
                              (datas['date'], datas['type'], datas['low'], datas['high'], datas['fengxiang'])
                    now_next_5_days_res.append(tmp_res)

                if recv[0] == '明天':
                    res = now_next_5_days_res[1]
                    await ser_weather.finish(res)
                if recv[0] == '昨天':
                    res = yes_res
                    await ser_weather.finish(res)
                if recv[0] == '预测':
                    res_ls = now_next_5_days_res
                    for res in res_ls:
                        await ser_weather.send(res)
                        time.sleep(0.5)
        else:
            res = '查天气使用方法\n/查天气 以显示当前温度和今日天气\n' \
                  '/查天气 明天 以显示明日天气\n' \
                  '/查天气 昨天 以显示昨日天气\n' \
                  '/查天气 预测 以显示五日（包括今天）天气\n' \
                  '/查天气 绑定 株洲 以将账号绑定查株洲天气\n' \
                  '/查天气 解绑 以解除地点绑定'
            await ser_weather.finish(res)
    elif len(recv) == 2 and recv[0] == '绑定':
        city = recv[1]
        if find_bd(qq_number):
            res = update(qq_number,city)
        else:
            res = insert(qq_number,city)
        await ser_weather.finish(res)
    elif len(recv) == 0:
        city = get_city(qq_number)
        if not get_city(qq_number):
            await ser_weather.finish('未绑定城市，请输入/查天气 绑定 城市名 以进行绑定')
        now_temperature, yesterday_data, forecast_datas = get_datas(city)
        datas = forecast_datas[0]
        res = '%s，%s\n当前的温度是%s\n%s\n%s\n风向：%s' % \
                  (datas['date'], datas['type'],now_temperature, datas['low'], datas['high'], datas['fengxiang'])
        await ser_weather.finish(res)


