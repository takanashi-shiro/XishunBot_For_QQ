import mysql.connector
SQL_config = {
    'user': 'root',
    'password': '2dErPVpn7hk9TXhv',
    'host': 'takanashi-shiro.top',
    'port': '33066',
    'database': 'qq_bot'
}


def link():
    con = mysql.connector.connect(**SQL_config)
    return con

def get_stus():
    sql = "select * from wmxy where daka = TRUE"
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    ls = []
    for i in results:
        dict_tmp = {
            'qq_number':i[0],
            'phone':i[1],
            'wmxy_passwd':i[2]
        }
        ls.append(dict_tmp)
    # print(ls)
    con.close()
    return ls

def exist_qq(qq_number):
    sql = "select qq_number from wmxy where qq_number = '%s'" % qq_number
    con = link()
    cursor = con.cursor(buffered=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    con.close()
    if result:
        return True
    else:
        return False

def update_stu(qq_number,phone,passwd):
    sql = "update wmxy set registed = 1,phone = '%s',wmxy_passwd = '%s' where qq_number = '%s'"%(qq_number,phone,passwd)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        res = "更新成功\n"
        print(res)
        con.close()
        return res
    except Exception as e:
        print(e)
        con.rollback()
        res = '更新失败，请重试！'
        con.close()
        return res

def insert_stu(qq_number,phone,wmxy_passwd='0'):
    sql = "insert into wmxy values('%s','%s','%s',0,0)" % (qq_number,phone,wmxy_passwd)
    con = link()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        print(e)
        con.rollback()
    return "绑定成功！\n您的信息如下：\n"+"账号: %s\n密码: %s"%(phone,wmxy_passwd)