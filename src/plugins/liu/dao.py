import requests
import os
import bs4
from .DB_Manage import get_numbers as get_liu_number, insert as insert_item


# from DB_Manage import get_numbers as get_liu_number, insert as insert_item


def get_title_by_bv(bv: str) -> str:
    comic = ''
    try:
        url = 'https://www.bilibili.com/video/BV' + bv
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        comic = soup.find_all('title')[0].text.strip('_哔哩哔哩_bilibili')
    except Exception as e:
        comic = str(e)
    finally:
        return comic


def dao_work(bv: str, p: str = '1'):
    try:
        path = '/music/'
        url = "https://api.injahow.cn/bparse?"
        headers = {
            'bv': bv,
            'p': p,
            'q': '64',
            'format': 'mp4',
            'otype': 'url'
        }
        true_title = get_title_by_bv(bv)
        # send_tmp_msg(true_title, group_id)

        for i in headers:
            url += '&' + i + '=' + headers[i]

        count_id = str(get_liu_number() + 1)

        title = 'liu' + count_id
        print('1')
        with open(path + '{}.mp4'.format(title), 'wb') as f:
            f.write(requests.get(
                requests.get(url).content
            ).content
                    )
        print('2')
        msg = insert_item(true_title, path + title + '.amr')
        os.system("ffmpeg -i {}.mp4 -ar 8000 -ab 12.2k -ac 1 {}.amr".format(path + title, path + title))
        os.system('rm {}.mp4'.format(path + title))
        # os.system('del {}.mp4'.format(path + title))

        return 'success', true_title, path + title + '.amr'

    except Exception as e:
        print(e)
        return str(e), '', ''


async def send_tmp_msg(send_msg_content: str, group_id):
    import nonebot.adapters.cqhttp
    from nonebot.adapters.onebot.v11 import MessageSegment
    bot = list(nonebot.get_bots().values())[0]
    await bot.send_group_msg(group_id=group_id, messages=MessageSegment.text("正在加载 " + send_msg_content + '中..'))


if __name__ == '__main__':
    print(dao_work('12q4y1T7DS'))
