device_seed = 18656102997

def rand():
    """
    种子计算 用于生成IMEI
    """
    global device_seed
    device_seed = (device_seed * 9301 + 49297) % 233280
    return device_seed / 233280.0

def generate_IMEI(seed):
    """
    生成IMEI
    """
    code = ''
    sum = 0
    for _ in range(12):
        code += str(int(rand()*10))
    data = '86' + code
    for index, ch in enumerate(data):
        if index % 2:
            ch = int(ch)*2
            sum += int(ch/10) + ch % 10
        else:
            sum += int(ch)
    data += str(sum * 9 % 10)
    return data

print(generate_IMEI(device_seed))

