import requests
import json
import time
import re
import random
import os

from .campus import CampusCard
from ..database import mysql_data
from ..login import push


def get_time():
    return [(time.localtime().tm_hour + 8) % 24,
            time.localtime().tm_min,
            time.localtime().tm_sec]


def get_token(phone, password, device_seed):
    stuobj = CampusCard(phone, password, device_seed).user_info
    if stuobj['login']:
        return stuobj["sessionId"]
    return None


def get_last_post_json(token):
    resp = requests.post(
        "https://reportedh5.17wanxiao.com/sass/api/epmpics",
        headers={
            "Host": "reportedh5.17wanxiao.com",
            "content-length": "134",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; U; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10)",
            "content-type": "application/json;charset\u003dUTF-8",
            "origin": "https://reportedh5.17wanxiao.com",
            "x-requested-with": "com.newcapec.mobile.ncp",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7",
        }, json={
            "businessType": "epmpics",
            "jsonData": {"templateid": "pneumonia", "token": token},
            "method": "userComeApp"
        },
    ).json()
    try:
        base = json.loads(resp['data'])
        data = {
            "deptStr": base['deptStr'],
            "areaStr": base['areaStr'],
            "reportdate": round(time.time() * 1000),
            "customerid": base['customerid'],
            "deptid": base['deptStr']['deptid'],
            "source": "app",
            "templateid": "pneumonia",
            "stuNo": base['stuNo'],
            "username": base['username'],
            "phonenum": "",
            "userid": base['userid'],
            'updatainfo': [],
            "gpsType": 1,
            "token": token
        }
        # print(base.keys())
        for i in base['cusTemplateRelations']:
            data['updatainfo'].append(
                {'propertyname': i['propertyname'], "value": i["value"]})
    except Exception as e:
        print(e)
        return None
    return data


def Do(phone, password, device_seed, qq_number):
    token = get_token(phone, password, device_seed)
    if not token:
        return '获取token失败'
    data = get_last_post_json(token)
    # print(data)
    if not data:
        return '获取上一次打卡信息失败'
    resp = requests.post(
        "https://reportedh5.17wanxiao.com/sass/api/epmpics",
        headers={
            "Host": "reportedh5.17wanxiao.com",
            "content-length": "134",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; U; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10)",
            "content-type": "application/json;charset\u003dUTF-8",
            "origin": "https://reportedh5.17wanxiao.com",
            "x-requested-with": "com.newcapec.mobile.ncp",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7",
        }, json={
            "businessType": "epmpics",
            "jsonData": data,
            "method": "submitUpInfo"
        },
    ).json()
    checkbox = []
    for key, value in data.items():
        dict_tmp = {
            'description': str(key),
            'value': str(value)
        }
        checkbox.append(dict_tmp)
    if resp['code'] == '10000':
        print(resp)
        push.wanxiao_qq_mail_push(
            send_email='764806602@qq.com',
            send_pwd='xsttyvproafkbaij',
            receive_email=qq_number + '@qq.com',
            check_info_list=[
                {
                    "status": True,
                    'post_dict': {
                        'username': qq_number,
                        'name': qq_number,
                        "checkbox": checkbox
                    },
                    "res": '打卡成功',
                    'errmsg': '出错'
                }
            ]
        )
        return None
    else:
        push.wanxiao_qq_mail_push(
            send_email='764806602@qq.com',
            send_pwd='xsttyvproafkbaij',
            receive_email=qq_number + '@qq.com',
            check_info_list=[
                {
                    "status": True,
                    'post_dict': {
                        'username': qq_number,
                        'name': qq_number,
                        "checkbox": checkbox
                    },
                    "res": '打卡失败',
                    'errmsg': '出错'
                }
            ]
        )
        return "打卡出现异常：" + resp['data']



def main():
    stus = mysql_data.get_stus()
    for stu in stus:
        phone = stu['phone']
        password = stu['wmxy_passwd']
        device_seed = phone
        qq_number = stu['qq_number']
        print(Do(phone, password, device_seed, qq_number))
        time.sleep(random.randint(30,180))


# 腾讯云函数从此入口进入
# def main_handler(arg1, arg2):
#     stus = []
#     i = 1
#     while True:
#         try:
#             user = os.environ.get('user' + str(i))
#             if user is None:
#                 break
#             stus.append(user.split(' '))
#             i += 1
#         except:
#             break
#     main(stus)

def qq_bot_run():
    stus = mysql_data.get_stus()
    print(stus)
    main()

# 直接运行脚本从此入口进入
if __name__ == "__main__":
    tmp = input()
    stus = mysql_data.get_stus()
    print(stus)

    main(stus)
