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
    source = ''
    ans = ''
    for i in reqs['trans_result']:
        source+=i['src']
        source+='\n'
        ans+=i['dst']
        ans+='\n'
    res = source+'\n翻译结果：\n'+ans
    print(res)
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
    msg_tmp = msg_tmp.replace('\r','')
    msg_tmp = msg_tmp.replace('\n','')
    msg_tmp = msg_tmp.replace('\t','')
    msg_tmp = msg_tmp.replace('\f','')
    if isalEng(msg_tmp):
        return trans_in_baidu(msg)

# if __name__ == '__main__':
#     s = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
#     print(translate(s))
