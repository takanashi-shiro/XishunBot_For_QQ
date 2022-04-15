import mysql.connector
from ..config import SQL_config as config


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
    sql = "select * from qq_yiqing where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    if len(result) != 0:
        return True
    else:
        return False


def insert(qq_number, city):
    if find_bd(qq_number):
        res = '该qq已经绑定了一个城市！'
        return res
    sql = "insert into qq_yiqing values ('%s','%s')" % (qq_number, city)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        res = "%s 绑定 %s 成功!" % (qq_number, city)
        print(res)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '绑定失败，请重试！'
        con.close()
        return res


def update(qq_number, city):
    sql = "update qq_yiqing set citys = '%s' where qq_number = '%s' " % (city, qq_number)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        res = "%s 更新城市 %s 成功!\n" % (qq_number, city)
        print(res)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '更新失败，请重试！'
        con.close()
        return res


def get_citys(qq_number):
    sql = "select citys from qq_yiqing where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        con.close()
        city = result[0]
        print(city)
        return city
    except Exception as e:
        print(e)
        res = 'qq未绑定城市或绑定出错，请重试！'
        con.close()
        return False


def unband(qq_number):
    sql = "delete from qq_yiqing where qq_number = '%s'" % qq_number
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

if __name__ == '__main__':
    print(insert('764806602','株洲'))
    print(get_city('764806602'))