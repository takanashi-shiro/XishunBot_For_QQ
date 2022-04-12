def get_simple_info(class_ls):
    res = []
    for item in class_ls:
        name_teacher = (item['name'],item['teacher'])
        if name_teacher not in res:
            res.append(name_teacher)
    return res


