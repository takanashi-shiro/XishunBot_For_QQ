import datetime
import random
import time
from typing import List, Any
import requests

import functools

from ..database.DB_Manage import get_users, update_sys
from ..login.login import get_token


def mycmp(a, b):
    if len(a['name']) > len(b['name']):
        if a['name'] < b['name']:
            return -1
        elif a['name'] > b['name']:
            return 1
        else:
            return 0
    elif len(a['name']) < len(b['name']):
        if a['name'] < b['name']:
            return 1
        elif a['name'] > b['name']:
            return -1
        else:
            return 0
    else:
        return 0
    # return a['name'] < b['name']


def choose_building(session):
    url = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoom.do?payProId=1567&schoolcode=786&optype=2&areaid=4&buildid=0&unitid=0&levelid=0&businesstype=2'
    headers = {
        'Host': 'h5cloud.17wanxiao.com:8080',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.5.8 CCBSDK/2.4.0',
        'Referer': 'http://h5cloud.17wanxiao.com:8080/CloudPayment/bill/selectPayProject.do?txcode=elecdetails&interurl=elecdetails&payProId=1567&amtflag=0&payamt=0&payproname=%E8%B4%AD%E7%94%B5%E6%94%AF%E5%87%BA&img=http://cloud.17wanxiao.com:8080/CapecYunPay/images/project/img-nav_2.png&subPayProId=',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    response = session.get(url, headers=headers)

    print(response.text)

    dicts = response.json()
    buildings = dicts['roomlist']
    tmp = sorted(buildings, key=functools.cmp_to_key(mycmp))
    namelist = []
    idlist = []
    for i in tmp:
        if i['name'].find('学生') != -1:
            namelist.append(i['name'])
            idlist.append(i['id'])
    res: list[list[Any]] = [namelist, idlist]
    return res

def choose_room(session,id):
    url = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoom.do?payProId=1567&schoolcode=786&optype=4&areaid=4&buildid='+id+'&unitid=0&levelid=-1&businesstype=2'
    headers = {
        'Host': 'h5cloud.17wanxiao.com:8080',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.5.8 CCBSDK/2.4.0',
        'Referer': 'http://h5cloud.17wanxiao.com:8080/CloudPayment/bill/selectPayProject.do?txcode=elecdetails&interurl=elecdetails&payProId=1567&amtflag=0&payamt=0&payproname=%E8%B4%AD%E7%94%B5%E6%94%AF%E5%87%BA&img=http://cloud.17wanxiao.com:8080/CapecYunPay/images/project/img-nav_2.png&subPayProId=',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    response = session.get(url=url,headers=headers)
    dicts = response.json()
    roomlist=dicts['roomlist']
    idlist = []
    namelist = []
    for i in roomlist:
        idlist.append(i['id'])
        namelist.append(i['name'])
    res: list[list[Any]] = [namelist, idlist]
    return res

def query_elc(session,id):
    url = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoomState.do?payProId=1567&schoolcode=786&businesstype=2&roomverify='+id
    headers = {
        'Host': 'h5cloud.17wanxiao.com:8080',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.5.8 CCBSDK/2.4.0',
        'Referer': 'http://h5cloud.17wanxiao.com:8080/CloudPayment/bill/selectPayProject.do?txcode=elecdetails&interurl=elecdetails&payProId=1567&amtflag=0&payamt=0&payproname=%E8%B4%AD%E7%94%B5%E6%94%AF%E5%87%BA&img=http://cloud.17wanxiao.com:8080/CapecYunPay/images/project/img-nav_2.png&subPayProId=',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    response = session.get(url=url,headers=headers)
    dicts = response.json()
    res = '寝室号：'+dicts['description']+'\n剩余电量：'+dicts['quantity']+'度\n'
    return res,str(dicts['quantity'])


def get_elc_main():
    stus = get_users()
    msg = ''
    for stu in stus:
        phone = stu['phone']
        pwd = stu['pwd']
        qq_number = stu['qq_number']
        building = stu['building']
        room = str(stu['room'])
        token = get_token(phone, pwd, phone)
        if token is None or token == 'None':
            msg += 'qq:%s\ntoken:%s\n' % (qq_number, token)
            continue
        url = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/pay.do?versioncode=10558102&systemType=IOS&UAinfo=wanxiao&token=' + token + '&customerId=786'
        session = requests.session()
        session.post(url)

        buildings = choose_building(session)[1]
        search_building = str(buildings[building])
        rooms = choose_room(session,search_building)
        room_id = str(rooms[1][rooms[0].index(room)])
        res1,res2 = query_elc(session,room_id)
        today_time = str(datetime.datetime.now()).split('.')[0]
        today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
        update_sys(qq_number,building,room,float(res2),today_time)
        print(res1)
        print(res2)
        time.sleep(random.randint(1,180))
    return msg


def get_elc(building,room):
    url = 'https://daohang.yixun.club/api/V1/elec.php'
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; MI 9 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220505 Mobile Safari/537.36 MMWEBID/5880 MicroMessenger/8.0.23.2160(0x28001757) WeChat/arm64 Weixin NetType/4G Language/en ABI/arm64',
        'content-type': 'application/json',
        'x-requested-with': 'com.tencent.mm',
        'referer': 'https://daohang.yixun.club/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en,en-US;q=0.9',
    }
    data = {
        "dongNum": str(building),
        "suNum": room,
        "quNum": "西"
    }
    session = requests.session()
    response = session.post(url=url, headers=headers, json=data)
    dicts = response.json()
    print(dicts)
    return dicts

def get_elc_main_second():
    stus = get_users()
    msg = ''
    for stu in stus:
        qq_number = stu['qq_number']
        building = stu['building']
        room = str(stu['room'])
        print(building,room)
        dicts = get_elc(building,room)
        res2 = dicts['resultData']['eledetail']
        today_time = str(datetime.datetime.now()).split('.')[0]
        today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
        update_sys(qq_number, building, room, float(res2)/0.6, today_time)
        msg += str(qq_number)+' success\n'
        # time.sleep(random.randint(1, 180))
    return msg

if __name__ == '__main__':
    get_elc_main_second()