import requests
import time
import random
def query_elc(id):
    url = 'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoomState.do?payProId=1567&schoolcode=786&businesstype=2&roomverify='+id
    response = requests.get(url=url)
    dicts = response.json()
    res = '寝室号：'+dicts['description']+'\n剩余电量：'+dicts['quantity']+'度\n'
    return res,str(dicts['quantity'])