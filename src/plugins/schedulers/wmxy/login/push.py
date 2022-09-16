import datetime
import json
from ..utils.server_chan import server_push
from ..utils.qq_email import qq_email_push
from ..utils.qmsg import qmsg_push


def wanxiao_server_push(sckey, check_info_list):  #  Server 酱的推送信息模块
    utc8_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    push_list = [f"""

------
#### 打卡时间：{utc8_time.strftime("%Y-%m-%d %H:%M:%S %p")}
"""]
    for check_info in check_info_list:
        if check_info["status"]:
            if check_info["post_dict"].get("checkbox"):
                post_msg = "\n".join(
                    [
                        f"| {i['description']} | {j['value']} |"
                        for i in check_info["post_dict"].get("checkbox")
                        for j in check_info["post_dict"].get("updatainfo")
                        if i["propertyname"] == j["propertyname"]
                    ]
                )
            else:
                post_msg = "暂无详情"
            name = check_info["post_dict"].get("username")
            if not name:
                name = check_info["post_dict"]["name"]
            push_list.append(
                f"""#### {name}{check_info['type']}打卡信息：
| 项目                           | 提交值 |
| :----------------------------------- | :--- |
{post_msg}
------
打卡结果：{check_info['res']}
"""
            )
        else:
            push_list.append(
                f"""------
#### {check_info['errmsg']}
------
"""
            )
    push_list.append(
        f"""
    >From~每次打卡附祝福 star✨
    >～早*⸜( •ᴗ• )⸝*安～
    >～祝愿你的今天又是开开心心的一天~
    >免责声明
    >不进行任何商业用途❤仅供学习交流使用
    >最新版代码已更新❤以提高打卡稳定性
    >打卡服务器:M27-KaLi
"""
    )
    return server_push(sckey, "健康打卡-点击查看详细信息", "\n".join(push_list))


def wanxiao_qq_mail_push(send_email, send_pwd, receive_email, check_info_list):  #  邮箱的信息推送模块
    bj_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    bj_time.strftime("%Y-%m-%d %H:%M:%S %p")
    mail_msg_list = [f"""
<h2 style="color:rgb(120, 32, 192);"><center>早*⸜( •ᴗ• )⸝*安</center></h2>
<h3 style="color:rgb(233, 148, 209);"><center>祝愿你的今天又是开开心心的一天~</center></h3>
<h3 style="color:rgb(233, 148, 209);"><center>打卡时间：{bj_time}</center></h3>
<a style="color:red;font-size: 24px;"><b><center>免责声明</center></b></a>
<a style="color:red;"><b><center>不进行任何商业用途&nbsp&nbsp·&nbsp&nbsp仅供学习交流使用</center></b></a>
<a style="color: coral;font-size: 18px;"><b><center>打卡服务器:Takanashi_Shiro</center></b></a>
"""
                     ]
    for check in check_info_list:
        if check["status"]:
            name = check['post_dict'].get('username')
            if not name:
                name = check['post_dict']['name']
            mail_msg_list.append(f"""<hr>
<a style="color:green;font-size: 14px;"><b><center>打卡结果：{check['res']}</center></b></a>
<hr>
<summary style="font-family: 'Microsoft YaHei UI',serif; color: lightskyblue;font-size: 8px;" ></summary>
<table id="customers">
<tr>
<th>项目</th>
<th>提交值</th>
</tr>
"""
                                 )
            for index, box in enumerate(check["post_dict"]["checkbox"]):
                if index % 2:
                    mail_msg_list.append(
                        f"""<tr>
<td>{box['description']}</td>
<td>{box['value']}</td>
</tr>"""
                    )
                else:
                    mail_msg_list.append(f"""<tr class="alt">
<td>{box['description']}</td>
<td>{box['value']}</td>
</tr>"""
                                         )
            mail_msg_list.append(
                f"""
</table>"""
            )
        else:
            mail_msg_list.append(
                f"""<hr>
    <b style="color: red">{check['errmsg']}</b>"""
            )
    css = """<style type="text/css">
#customers
  {
  font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
  width:100%;
  border-collapse:collapse;
  }

#customers td, #customers th
  {
  font-size:1em;
  border:1px solid #98bf21;
  padding:3px 7px 2px 7px;
  }

#customers th
  {
  font-size:1.1em;
  text-align:left;
  padding-top:5px;
  padding-bottom:4px;
  background-color:#A7C942;
  color:#ffffff;
  }

#customers tr.alt td
  {
  color:#000000;
  background-color:#EAF2D3;
  }
</style>"""
    mail_msg_list.append(css)
    return qq_email_push(send_email, send_pwd, receive_email,
                         title="完美校园健康打卡", text="".join(mail_msg_list))


def wanxiao_qmsg_push(key, qq_num, check_info_list, send_type):    #  Qmsg的信息推送模块
    utc8_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    push_list = [f'@face=74@ {utc8_time.strftime("%Y-%m-%d %H:%M:%S")} @face=74@ ']
    for check_info in check_info_list:
        if check_info["status"]:
            name = check_info["post_dict"].get("username")
            if not name:
                name = check_info["post_dict"]["name"]
            push_list.append(f"""\
@face=54@ {name}{check_info['type']} @face=54@
@face=211@
{check_info['res']}
@face=211@""")
        else:
            push_list.append(check_info['errmsg'])
    return qmsg_push(key, qq_num, "\n".join(push_list), send_type)
