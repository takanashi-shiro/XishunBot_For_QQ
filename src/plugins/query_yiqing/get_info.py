import requests
import json
import time

# 观察开发者工具network找到url

cn_url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'

def get_cn_page(page_cn):  # 请求中国疫情数据
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        resp = requests.get(url=page_cn,headers=headers)
        # print(resp.json()['data']['areaTree'][2]['children'][5])
        resp.encoding = resp.apparent_encoding
        status = resp.status_code
        if status == 200:
            return json.loads(resp.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)


def parse_province_page(items_cn):  # 解析中国各省疫情数据
    province_list = []
    province_items = items_cn['data']['areaTree'][2]['children']
    children_list = []
    for province_item in province_items:
        province_name = province_item['name']  # 省份
        province_date = items_cn['data']['lastUpdateTime']  # 当前日期
        province_confirm = province_item['total']['confirm']  # 累计确诊
        province_dead = province_item['total']['dead']  # 累计死亡
        province_heal = province_item['total']['heal']  # 累计治愈
        province_nowConfirm = province_confirm - province_dead - province_heal  # 现有确诊
        province_confirm_add = province_item['today']['confirm']  # 当日新增确诊
        province_children_items = province_item['children']
        for i in range(0, len(province_children_items)):
            province_children_items[i]['province'] = province_name
        province_dic = {'省份': province_name, '日期': province_date,
                        '累计确诊': province_confirm, '累计死亡': province_dead,
                        '累计治愈': province_heal, '现有确诊': province_nowConfirm,
                        '当日新增确诊': province_confirm_add}
        province_list.append(province_dic)
        children_list.append(province_children_items)
    return province_list, children_list


def get_city(items_cn, province_children_items):
    city_list = []
    for city_items in province_children_items:
        for city_item in city_items:
            city_name = city_item['name']  # 市(区)
            city_date = items_cn['data']['lastUpdateTime']  # 当前日期
            city_confirm = city_item['total']['confirm']  # 累计确诊
            city_dead = city_item['total']['dead']  # 累计死亡
            city_heal = city_item['total']['heal']  # 累计治愈
            city_nowConfirm = city_confirm - city_dead - city_heal  # 现有确诊
            city_confirm_add = city_item['today']['confirm']  # 当日新增确诊
            city_province = city_item['province']

            city_dic = {'省份': city_province, '市(区)': city_name, '日期': city_date,
                        '累计确诊': city_confirm, '累计死亡': city_dead,
                        '累计治愈': city_heal, '现有确诊': city_nowConfirm,
                        '当日新增确诊': city_confirm_add}
            city_list.append(city_dic)
    return city_list


def get_province_name_list(p_list):
    p_name_list = []
    for i in p_list:
        p_name_list.append((i['省份']))
    return p_name_list


def get_city_name_list(city_list):
    city_name_list = []
    for i in city_list:
        city_name_list.append(i['市(区)'])
    while '地区待确认' in city_name_list:
        city_name_list.remove('地区待确认')
    while '境外输入' in city_name_list:
        city_name_list.remove('境外输入')
    while '境外来沪' in city_name_list:
        city_name_list.remove('境外来沪')
    while '外地来沪' in city_name_list:
        city_name_list.remove('外地来沪')
    while '待确认' in city_name_list:
        city_name_list.remove('待确认')
    while '外地来京' in city_name_list:
        city_name_list.remove('外地来京')
    while '涉奥闭环人员' in city_name_list:
        city_name_list.remove('涉奥闭环人员')
    return city_name_list


def get_order_province(province_name,p_list):
    res = '没有找到'
    for item in p_list:
        if item['省份'] == province_name:
            res = item
    return res


def get_order_city(city_name,city_list):
    res = '没有找到'
    for item in city_list:
        if item['市(区)'] == city_name:
            res = item
    return res

# if __name__ == '__main__':
#     cn_data = get_cn_page(cn_url)
#     p_list, p_children = parse_province_page(cn_data)
#     city_list = get_city(cn_data, p_children)
#     city_name_list = get_city_name_list(city_list)
#     province_name_list = get_province_name_list(p_list)
#
#     province_input = '湖南'
#     order_province_info = get_order_province(province_input,p_list)
#
#     city_input = '株洲'
#     order_city_info = get_order_city(city_input,city_list)
#     print(order_city_info)
