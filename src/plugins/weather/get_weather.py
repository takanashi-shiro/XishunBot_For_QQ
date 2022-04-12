import requests
import random
import json


def get_datas(city_name):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city_name
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    # print(response.text)
    datas = json.loads(response.text).get('data')
    yesterday_datas = datas.get('yesterday')
    forecast_datas = datas.get('forecast')
    now_temperature = datas.get('wendu') + '℃'
    # print(forecast_datas)
    # print(now_temperature)
    # print(yesterday_datas)
    return now_temperature,yesterday_datas,forecast_datas


if __name__ == '__main__':
    now_temperature,yesterday_data,forecast_datas = get_datas('株洲')
    yes_res = '昨天是%s，%s\n%s\n%s\n风向：%s' % \
              (yesterday_data['date'],yesterday_data['type'],yesterday_data['low'],yesterday_data['high'],yesterday_data['fx'])
    now_next_5_days_res = []
    for datas in forecast_datas:
        tmp_res = '%s，%s\n%s\n%s\n风向：%s' % \
                  (datas['date'],datas['type'],datas['low'],datas['high'],datas['fengxiang'])
        now_next_5_days_res.append(tmp_res)
    print(yes_res)
    print(now_next_5_days_res)