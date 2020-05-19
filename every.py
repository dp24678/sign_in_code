# _*_coding:utf-8 _*_
import requests
import re
import logging
import time



def main():
    logging.basicConfig(
        filename='itcast_sign_in.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    logging.info("======start app======\n\n")
    sission_ = requests.Session()
    login_page_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    login_page_url = "http://bbs.itheima.com/member.php?mod=logging&action=login"
    login_page_res = sission_.get(login_page_url, headers=login_page_headers)
    formhash1 = re.search(r'type="hidden" name="formhash" value="(.*?)" />',login_page_res.text).group(1)

    login_url = "http://bbs.itheima.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LJci8&inajax=1"
    login_headers = {
        "Referer": "http://bbs.itheima.com/member.php?mod=logging&action=login",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    data = {
        "formhash": formhash1,
        "referer": "http://bbs.itheima.com/forum.php",
        "username": "646595307@qq.com",
        "password": "cb1768fea108ffd811a7a4607f917600",
        "questionid": "0",
        "answer": ""
    }
    res2 = sission_.post(login_url,headers=login_headers, data=data)
    if "现在将转入登录前页面" in res2.text:
        logging.info("======Login successfully======\n\n")
    else:
        logging.info("======Login failed======\n\n")

    forum_page_url = "http://bbs.itheima.com/forum.php"
    forum_page_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    res3 = sission_.get(forum_page_url,headers=forum_page_headers)
    formhash3 = re.search(r'type="hidden" name="formhash" value="(.*?)" />', res3.text).group(1)

    sgin_url = "http://bbs.itheima.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
    sgin_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": 'zh-CN,zh;q=0.9',
        "Cache-Control": 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': "48",
        'Content-Type': "application/x-www-form-urlencoded",
        "Host": "bbs.itheima.com",
        "Origin": "http://bbs.itheima.com",
        "Referer": "http://bbs.itheima.com/forum.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"""
    }
    sign_data = {
        "formhash": formhash3,
        "qdxq": "kx",  # 签到心情，kx：开心
        "qdmode": "3",  # 签到方式
        "todaysay": "",  # 今日想说 内容
        "fastreply": "0"  # 快速回复
    }
    res4 = sission_.post(url=sgin_url,data=sign_data,headers=sgin_headers)
    res_str = res4.text
    if "恭喜你签到成功" in res_str:
        logging.info("======Sign in successfully======\n\n")
    elif "您今日已经签到，请明天再来" in res_str:
        logging.info("======Already signed in======\n\n")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(3600*12)

