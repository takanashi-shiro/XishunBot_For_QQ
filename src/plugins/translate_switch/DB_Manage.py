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

def update(qq_number, status):
    sql = "update trans_switch set switchs = '%d' where qq_number = '%s' " % (status, qq_number)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        if status:
            tmp = '开启'
        else:
            tmp = '关闭'
        res = "%s 修改状态为%s\n" % (qq_number,tmp)
        print(res)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '更新失败，请重试！'
        con.close()
        return res


def get_status(qq_number):
    sql = "select switchs from trans_switch where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        con.close()
        status = result[0]
        return status
    except Exception as e:
        print(e)
        res = '更新出错，请重试！'
        con.close()
        return False

# if __name__ == '__main__':
#     print(type(get_status('764806602')))