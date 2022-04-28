import mysql.connector
from ..config import SQL_config as config


def link():
    con = mysql.connector.connect(**config)
    return con


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