import mysql.connector
import datetime
from ...config import SQL_config as config


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

def get_users():
    sql = "select q.qq_number,q.building,q.room from query_elc as q"
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        con.close()
        ls = []
        for result in results:
            dict_tmp = {
                'qq_number':result[0],
                'building':result[1],
                'room':result[2]
            }
            ls.append(dict_tmp)
        return ls
    except Exception as e:
        print(e)
        res = '获取失败'
        print(res)
        con.close()
        return None

def insert(qq_number, building, room, elc):
    today_time = str(datetime.datetime.now()).split('.')[0]
    today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')

    sql = "insert into query_elc values('%s',%d,%d,%f,%f,'%s','%s')" % (
        qq_number, eval(building), eval(room), elc, elc, today_time, today_time)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        res = "%s 绑定 %s 栋 %s 成功!\n" % (qq_number, building, room)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '绑定失败，请重试！'
        con.close()
        return res

def update_sys(qq_number, building, room, elc, time):
    sql = "update query_elc set elc_now = %f,now_time = '%s' where qq_number = '%s' " % (elc, time, qq_number)
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

def update_user(qq_number, building, room, elc, time):
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
    # today_time = str(datetime.datetime.now()).split('.')[0]
    # today_time = datetime.datetime.strptime(today_time, '%Y-%m-%d %H:%M:%S')
    sql = "select building,room,elc_now,elc_pre,now_time,pre_time from query_elc where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        con.close()
        elc_now = result[2]
        elc_pre = result[3]
        now_time = result[4]
        pre_time = result[5]
        days = '0'
        interval_time = str(now_time - pre_time).split(',')
        if len(interval_time) == 2:
            days = interval_time[0].replace(' days', '')
            days = days.replace(' day', '')
            tmp = datetime.datetime.strptime(interval_time[1].strip(), '%H:%M:%S')
            hours = str(tmp.hour)
            minutes = str(tmp.minute)
            seconds = str(tmp.second)
        else:
            tmp = datetime.datetime.strptime(interval_time[0].strip(), '%H:%M:%S')
            hours = str(tmp.hour)
            minutes = str(tmp.minute)
            seconds = str(tmp.second)
        res = '寝室号：%s\n剩余电量: %s 度\n剩余金额: %s 元\n距离上次查询已经过去了%s天%s小时%s分钟%s秒\n与上次查询相比用了: %s 度\n花费金额为 %s 元\n' % (
            result[1], str(elc_now), '{:.2f}'.format(elc_now * elc_unit_price), days, hours, minutes, seconds, '{:.2f}'.format(elc_pre-elc_now), '{:.2f}'.format((elc_pre-elc_now+0.000001) * elc_unit_price))
        update_user(qq_number,result[0],result[1],elc_now,now_time)
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
