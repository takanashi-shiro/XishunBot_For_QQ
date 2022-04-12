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


def get_numbers():
    sql = "select count(liu_id) from liu"
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    res = cursor.fetchone()
    # print(res)
    cnt = res[0]
    return int(cnt)


def get_one_liu_by_id(song_id) -> tuple:
    pass


def insert(liu_title, liu_path) -> str:
    """大国工匠"""
    sql = "insert into liu(liu_title,liu_path) VALUES ('%s','%s')" % (liu_title, liu_path)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        con.close()
        msg = '  成功！'
    except Exception as e:
        print(e)
        con.rollback()
        con.close()
        msg = '  失败！'
    finally:
        return '添加  ' + liu_title + msg


