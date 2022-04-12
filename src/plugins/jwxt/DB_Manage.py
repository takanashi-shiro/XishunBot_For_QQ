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


def qq_to_cookie(qq_number, cookie):
    sql = "insert into jwxt values('%s','%s')" % (cookie, qq_number)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        print(e)
        con.rollback()
    return "绑定成功\n该系统仅存储cookies\n您的cookies如下：\n"+cookie


def update(qq_number, cookie):
    sql = "update jwxt set cookie = '%s' where qq_number = '%s'" % (cookie, qq_number)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        res = "更新cookie成功!\n%s 对应的cookie为 %s" % (qq_number, cookie)
        print(res)
        con.commit()
    except:
        con.rollback()
        print("更新失败!")
    return res


def is_qq_exist(qq_number):
    sql = "select qq_number from jwxt where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    flag = result == None
    con.close()
    return flag


def get_ls():
    sql = "select qq_number,cookie from jwxt"
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    resultset = cursor.fetchall()
    qq_ls = []
    cookies = []
    for item in resultset:
        qq_ls.append(item[0])
        cookies.append(item[1])
    ls_dict = dict(zip(qq_ls, cookies))
    res = dict(reversed(sorted(ls_dict.items())))
    con.close()
    return res

# def insert_class(class_name,teacher):
#     sql1 = "select MAX(class_id) from jwxt_class"
#     con = link()
#     cursor = con.cursor(buffered=True)
#     try:
#         cursor.execute(sql1)
#         cnt = cursor.fetchone()
#         if cnt == None:
#             cnt = 1
#         else:
#             cnt += 1
#         sql = "insert into jwxt_class values('%d','%s','%s')" % (cnt, class_name, teacher)
#         cursor.execute(sql)
#         con.commit()
#     except Exception as e:
#         print(e)
#         con.rollback()
#     return