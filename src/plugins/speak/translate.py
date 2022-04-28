#每月前200万字符免费
import requests
import hashlib
import json
True_ls = []

def trans_in_baidu(s:str):
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    appid = '20220427001193137'
    salt = '114514314'
    ps_key = 'gQUdtuIdyyfvJFHV0JQU'
    sign = appid+s+salt+ps_key
    hl = hashlib.md5()
    hl.update(sign.encode(encoding='utf-8'))
    sign = hl.hexdigest()
    params = {
        'q': s,
        'from': 'en',
        'to': 'zh',
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    req = requests.get(url,params=params)
    reqs = json.loads(req.text)
    res = reqs['trans_result'][0]['src']+'\n翻译结果：\n'+reqs['trans_result'][0]['dst']
    return res

def isalEng(s:str):
    cnt = 0
    if s[:3] == '[CQ' or s[:4] == 'http':
        return False
    for i in s:
        if i.isalpha():
            cnt+=1
        if i not in True_ls:
            return False
    if ((cnt/len(s)) < 0.5):
        print(cnt/len(s))
        return False
    return True

def translate(msg:str):
    if not True_ls:
        for i in range(21,127):
            if i in [23,26,60]:
                continue
            True_ls.append(chr(i))
        True_ls.append('\n')
    msg_tmp = msg.replace(' ','')
    if isalEng(msg_tmp):
        return trans_in_baidu(msg)

# if __name__ == '__main__':
#     if not True_ls:
#         for i in range(21,127):
#             True_ls.append(chr(i))
#         True_ls.append('\n')
#     s = "The peer-to-peer (often abbreviated P2P) is a model of interprocess communication whose properties provide striking contrasts to the client/server model. P2P model involves two processes, rather than a client and a server, that execute on a temporary basis communicating as equals.\n" \
#         "The P2P model is also a popular means of sharing files via the Internet. These items will be transferred between the two parties using the P2P model. However, this way of data transmission makes legal efforts to enforce copyright laws more difficult.\n" \
#         "The term peer-to-peer refers to a system by which two processes communicate over a network (or internet). It is not a property of the network (or internet). A process might use the P2P model to communicate with another process and later use the client/server model to communicate with another process over the same network."
#     print(isalEng(s))