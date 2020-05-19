# _*_coding:utf-8 _*_
#@Time    :2019/4/22 13:52
import requests
import re
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 邮件预警系统相关信息
MAIL_CONFIG = {
    'sender_email':'13503998870@163.com', #发送预警邮件的邮箱账号
    'sender_password':'wangyi123',  #邮箱授权码
    'receive_email':'248312738@qq.com',  #要接收邮件的地址
    'mail_title':'定时任务提醒',  #邮件标题
}


class EmailHandler(object):
    def __init__(self,sender_email,sender_password, type = 0):
        """
        :param sender_email:str 发送人邮箱地址（用户名）
        :param sender_password:str 发送人在QQ或163申请的授权码
        :param type:int 1 为QQ邮箱 0 为163邮箱
        """
        self.__QQ = {'smtp':'smtp.qq.com','port':465}
        self.__163 = {'smtp':'smtp.163.com','port':25}
        self.sender_email = sender_email
        self.sender_password = sender_password
        if type == 0:
           self.server=smtplib.SMTP(self.__163['smtp'],self.__163['port'])
           self.server.login (self.sender_email,self.sender_password)
        elif type == 1:
           self.server=smtplib.SMTP(self.__QQ['smtp'],self.__QQ['port'])
           self.server.login (self.sender_email,self.sender_password)


    def send_mail(self,To,subject,content):
        """
        :param To:str 接收人邮箱地址
        :param subject:str 邮件标题
        :param content:str 邮件内容
        :return:bool True 成功 False 失败
        """
        try:
            msg = MIMEText(content,'plain','utf-8')
            msg['From'] = formataddr(['黑马论坛签到任务执行成功',self.sender_email])
            msg['To'] = formataddr(['',To])
            msg['Subject'] = subject

            self.server.sendmail(self.sender_email,To,msg.as_string())
            print("【%s】邮件发送成功"%subject)
            return True
        except Exception as e:
            print("【%s】邮件发送失败,请检查信息：%s"%(subject,e))
            return False





def main():
    logging.basicConfig(
        filename='itcast_sign_in.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    # 1、访问登录页
    logging.info("====== start sign in ======")
    sission_ = requests.Session()
    login_page_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    login_page_url = "http://bbs.itheima.com/member.php?mod=logging&action=login"
    login_page_res = sission_.get(login_page_url, headers=login_page_headers)
    formhash1 = re.search(r'type="hidden" name="formhash" value="(.*?)" />',login_page_res.text).group(1)

    # 2、登录请求
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
        print("登录成功")
        logging.info("======Login successfully======")
    else:
        print("登录失败")
        logging.info("======Login failed======")

    # 3、重新进入社区主页
    forum_page_url = "http://bbs.itheima.com/forum.php"
    forum_page_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    res3 = sission_.get(forum_page_url,headers=forum_page_headers)
    formhash3 = re.search(r'type="hidden" name="formhash" value="(.*?)" />', res3.text).group(1)

    # 4、签到请求
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
        print("恭喜你签到成功")
        logging.info("======Sign in successfully======\n\n")
        emailer.send_mail(MAIL_CONFIG['receive_email'], MAIL_CONFIG['mail_title'], "---黑马论坛签到任务执行成功---\n===Sign in successfully===")
    elif "您今日已经签到，请明天再来" in res_str:
        print("您今日已经签到，请明天再来")
        logging.info("======Already signed in======\n\n")
        emailer.send_mail(MAIL_CONFIG['receive_email'], MAIL_CONFIG['mail_title'],
                          "---黑马论坛签到任务执行成功---\n===Already signed in===")


if __name__ == '__main__':
    emailer = EmailHandler(MAIL_CONFIG['sender_email'], MAIL_CONFIG['sender_password'])
    while True:
        time_now = time.strftime("%H", time.localtime())  # 刷新
        if time_now == "13":  # 此处设置每天定时的时间  7点执行
            subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 定时发送测试"
            print(subject)
            main()



        print('sleep 3600s')
        time.sleep(3600)

