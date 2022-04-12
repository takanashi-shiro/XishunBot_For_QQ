import random
import os


def liu2():
    a = random.randint(1, 100)
    path1 = "file:/root/music/new_music"
    path = '/music'
    files = os.listdir(path)
    cnt = len(files)
    ls = []
    for i in range(0, cnt):
        tmp = f'{path1}/' + files[i]
        ls.append(tmp)
    for i in range(0, cnt):
        files[i] = files[i].replace('.amr', '')
    res = "请欣赏金曲：" + files[a % cnt]
    res2 = ls[a % cnt]
    print(ls)
    return res, res2, ls, files


def true_liu():
    random_number = random.randint(1, 100)
    path = '/music'



if __name__ == "__main__":
    tmp = liu2()
    print(tmp[0])
    print(tmp[1])
