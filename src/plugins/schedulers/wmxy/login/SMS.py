from campus import login_by_SMS

# 此脚本用于验证虚拟设备
# device_seed输入任意数字
# 密码登陆时需传入相同的device seed

print('phone:', end="")
username = input()

t = login_by_SMS(username, username)
t.sendSMS()

print('SMS code:', end="")
t.authSMS(input())
