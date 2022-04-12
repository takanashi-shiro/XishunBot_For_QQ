import mysql.connector
from .get_now_grade import get_now_grade
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


def ser(username):
    sql = "select cf_grade,cf_max_grade from codeforce where cf_username = '%s'" % username
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    grade = (result[0],result[1])
    con.close()
    return grade


def get_ls():
    sql = "select cf_username,cf_grade,cf_max_grade from codeforce Order by cf_grade desc "
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    resultset = cursor.fetchall()
    name_ls = []
    grade_ls = []
    for item in resultset:
        name_ls.append(item[0])
        grade_ls.append((item[1], item[2]))
    ls_dict = dict(zip(name_ls, grade_ls))
    res = dict(reversed(sorted(ls_dict.items(), key=lambda i: i[1])))
    con.close()
    return res



def add(qq_number, username):
    grade = get_now_grade(username)
    now_grade = eval(grade[0])
    max_grade = eval(grade[1])
    sql = "insert into codeforce values('%s','%s',%d,%d)" % (qq_number, username, now_grade, max_grade)
    con = link()
    cursor = con.cursor()
    res = ''
    try:
        cursor.execute(sql)
        con.commit()
        res = '添加成功！\n' + username + '\n目前分数 : ' + str(now_grade) + '\n最高分数 : ' + str(max_grade)
        print(res)
        con.close()
        return res
    except Exception as e:
        con.rollback()
        print(e)
        res = '添加失败，请重试！'
        con.close()
        return res


def rm(username):
    sql = "delete from codeforce where cf_username = '%s'" % username
    con = link()
    cursor = con.cursor()
    res = ''
    try:
        cursor.execute(sql)
        con.commit()
        res = '删除'+username+'成功！'
        con.close()
        return res
    except:
        con.rollback()
        res = '删除失败，请重试！'
        con.close()
        return res


def update():
    tmp = get_ls()
    name_ls = tmp.keys()
    con = link()
    cursor = con.cursor()
    cnt = 0
    for i in name_ls:
        grade = get_now_grade(i)
        sql = "update codeforce set cf_grade = %d, cf_max_grade = %d where cf_username = '%s'" % (eval(grade[0]), eval(grade[1]), i)
        try:
            cursor.execute(sql)
            print("更新" + i + "成功!")
            cnt += 1
            con.commit()
        except:
            con.rollback()
            print("更新" + i + "失败!")
    return "更新成功了%d/%d条" % (cnt, len(name_ls))
