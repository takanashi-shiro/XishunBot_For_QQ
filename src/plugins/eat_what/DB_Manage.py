import mysql.connector
from ..config import SQL_config as config


def link():
    con = mysql.connector.connect(**config)
    return con


def get_id_ls():
    sql = "select food_id from food"
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    resultset = cursor.fetchall()
    res = []
    for item in resultset:
        res.append(item[0])
    con.close()
    return res


def get_now_id():
    sql = "select food_id from food"
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    resultset = cursor.fetchall()
    cnt = 1
    res = len(resultset)+1
    for item in resultset:
        if cnt != item[0]:
            res = cnt
            print(res)
            break
        cnt += 1
    con.close()
    return res


def add(name, place='暂无数据'):
    id = get_now_id()
    print(id)
    sql = "insert into food values(%d,'%s','%s')" % (id, name, place)
    con = link()
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        con.commit()
        res = '添加成功！\n名称: %s\n位置: %s' % (name, place)
        print(res)
        con.close()
        return res
    except Exception as e:
        con.rollback()
        print(e)
        res = '添加失败，请重试！'
        con.close()
        return res


def get_ls():
    sql = "select food_name, food_place from food ORDER BY food_id"
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    resultset = cursor.fetchall()
    name_ls = []
    place_ls = []
    for item in resultset:
        name_ls.append(item[0])
        place_ls.append(item[1])
    con.close()
    return name_ls, place_ls


def rm(id):
    sql = "delete from food where food_id = %d" % id
    con = link()
    cursor = con.cursor()
    res = ''
    try:
        cursor.execute(sql)
        con.commit()
        res = '删除成功！'
        con.close()
        return res
    except:
        con.rollback()
        res = '删除失败，请重试！'
        con.close()
        return res


def update(id, name='', place=''):
    res = ''
    s = 'food_name = %s,food_place = %s'
    if name == '':
        s = "food_place = '%s'" % place
    elif place == '':
        s = "food_name = '%s'" % name
    con = link()
    cursor = con.cursor()
    sql = "update food set %s where food_id = %d" % (s, id)
    print(sql)
    try:
        cursor.execute(sql)
        print("更新成功!")
        res = "更新成功!"
        con.commit()
        return res
    except:
        con.rollback()
        res = "更新失败!"
        print("更新失败!")
        return res

# if __name__=="__main__":
#     add('肯德基')
