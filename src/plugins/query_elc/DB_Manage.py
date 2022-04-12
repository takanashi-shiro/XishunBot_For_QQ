import mysql.connector
import datetime
from .choose_building import choose_building
from .choose_room import choose_room
from .query_elc import query_elc

config = {
    'user': 'root',
    'password': '2dErPVpn7hk9TXhv',
    'host': 'takanashi-shiro.top',
    'port': '33066',
    'database': 'qq_bot'
}

elc_unit_price = 0.6

def link():
    con = mysql.connector.connect(**config)
    return con


def to_user(qq_number):
    sql = "insert into user values(%s)" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        print(e)
        con.rollback()


def find_bd(qq_number):
    sql = "select * from query_elc where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    if len(result) != 0:
        return True
    else:
        return False


def get_elc(building, room):
    building = eval(building) - 1
    search = str(choose_building()[1][building])
    room_id = str(choose_room(search)[1][choose_room(search)[0].index(room)])
    elc = eval(query_elc(room_id)[1])
    return elc


def insert(qq_number, building, room):
    if find_bd(qq_number):
        res = '该qq已经绑定了一个房间！'
        return res

    today_time = str(datetime.datetime.now()).split('.')[0]
    today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')

    elc = get_elc(building, room)
    sql = "insert into query_elc values('%s',%d,%d,%f,%f,'%s','%s')" % (
        qq_number, eval(building), eval(room), elc, elc, today_time, today_time)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        res = "%s 绑定 %s 栋 %s 成功!" % (qq_number, building, room)
        print(res)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '绑定失败，请重试！'
        con.close()
        return res


def update(qq_number, building, room, elc, time):
    sql = "update query_elc set elc_pre = %f,pre_time = '%s' where qq_number = '%s' " % (elc, time, qq_number)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        res = "更新%s栋%s 成功\n" % (building, room)
        print(res)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '更新失败，请重试！'
        con.close()
        return res


def ser_by_qq(qq_number):
    today_time = str(datetime.datetime.now()).split('.')[0]
    today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
    sql = "select building,room,elc_pre,pre_time from query_elc where qq_number = '%s'" % qq_number
    print(sql)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        con.close()
        elc_pre = result[2]
        pre_time = result[3]
        days = '0'
        interval_time = str(today_time - pre_time).split(',')
        if len(interval_time) == 2:
            days = interval_time[0].replace(' days', '')
            tmp = datetime.datetime.strptime(interval_time[1].strip(), '%H:%M:%S')
            hours = str(tmp.hour)
            minutes = str(tmp.minute)
            seconds = str(tmp.second)
        else:
            tmp = datetime.datetime.strptime(interval_time[0].strip(), '%H:%M:%S')
            hours = str(tmp.hour)
            minutes = str(tmp.minute)
            seconds = str(tmp.second)
        elc = get_elc(str(result[0]), str(result[1]))
        print(elc)
        print(elc_pre)
        res = '寝室号：%s\n剩余电量: %s 度\n剩余金额: %s 元\n距离上次查询已经过去了%s天%s小时%s分钟%s秒\n与上次查询相比用了: %s 度\n花费金额为 %s 元\n' % (
            result[1], str(elc), '{:.2f}'.format(elc * elc_unit_price), days, hours, minutes, seconds, '{:.2f}'.format(elc_pre-elc), '{:.2f}'.format((elc_pre-elc+0.000001) * elc_unit_price))
        update(qq_number, result[0], result[1], elc, today_time)
        return res
    except Exception as e:
        print(e)
        res = '查询失败，可能是qq未绑定房间，请重试！'
        con.close()
        return res


def unband(qq_number):
    sql = "delete from query_elc where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        con.close()
        res = '解除绑定成功!'
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '解除绑定失败，可能没有进行绑定'
        con.close()
        return res
