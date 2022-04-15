from nonebot import *
from nonebot.adapters.onebot.v11 import Event
from nonebot.typing import T_State
from nonebot.params import State

from .DB_Manage import *
from .get_info import *

query_yq = on_command('查疫情',block=True)
# 查疫情  查询当前绑定地区
# 查疫情 绑定 [地区]
# 查疫情 [地区]
def get_res(order_info) -> str:
    res = '日期: %s \n' \
          '%s 的疫情状况\n' \
          '%s : %d\n' \
          '%s : %d\n' \
          '%s : %d\n' \
          '%s : %d\n' \
          '%s : %d\n' \
          % (order_info['日期'],
             order_info['省份'],
             '累计确诊', order_info['累计确诊'],
             '累计死亡', order_info['累计死亡'],
             '累计治愈', order_info['累计治愈'],
             '现有确诊', order_info['现有确诊'],
             '当日新增确诊', order_info['当日新增确诊'])
    return res


@query_yq.handle()
async def query_yq_main(bot: Bot, event: Event, state: T_State = State()):
    recv = str(event.message).split()
    recv.pop(0)
    cn_data = get_cn_page(cn_url)
    p_list, p_children = parse_province_page(cn_data)
    city_list = get_city(cn_data, p_children)
    city_name_list = get_city_name_list(city_list)
    province_name_list = get_province_name_list(p_list)
    qq_number = str(event.get_user_id())

    if len(recv) == 2 and str(recv[0]) == '绑定':
        city = recv[1]
        if city not in city_name_list and city not in province_name_list:
            await query_yq.finish('输入地区有误，请重新输入')
        else:
            if find_bd(qq_number):
                res = update(qq_number, city)
            else:
                res = insert(qq_number, city)
            await query_yq.finish(res)
    elif len(recv) == 1:
        city = recv[0]
        if city not in city_name_list and city not in province_name_list:
            await query_yq.finish('输入地区有误，请重新输入')
        else:
            if city in province_name_list:
                order_info = get_order_province(city, p_list)
            else:
                order_info = get_order_city(city, city_list)
            res = get_res(order_info)
            await query_yq.finish(res)
    elif len(recv) == 0:
        city = get_city(qq_number)
        if city not in city_name_list and city not in province_name_list:
            await query_yq.finish('地区有误，请重新绑定')
        else:
            if city in province_name_list:
                order_info = get_order_province(city, p_list)
            else:
                order_info = get_order_city(city, city_list)
            res = get_res(order_info)
            await query_yq.finish(res)


