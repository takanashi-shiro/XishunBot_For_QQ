from urllib.parse import urlencode


def baidu(msg:str):
    ask_msg = None
    end_char = ['是啥','是什么','是谁']
    start_char = ['什么是','啥是','啥叫','什么叫','为什么','为啥']
    for char in end_char:
        if msg.endswith(char):
            ask_msg = msg[:-len(char)]
            break
    for char in start_char:
        if msg.startswith(char):
            ask_msg = msg[len(char):]
            break
    if ask_msg:
        param = {
            'wd': ask_msg
        }
        search_url = f'建议百度: https://www.baidu.com/s?{urlencode(param)}'
        return search_url
    return None
