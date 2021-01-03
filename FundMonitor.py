import json
import smtplib
import time
from datetime import date
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *

def fundMonitor():
    print("基金监控启动成功!")
    text = ''
    flag = 1
    times = 0
    while flag == 1 and times < 6:
        flag = 0
        for holdFund in fundList:
            f = requests.get(
                'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol={}'.format(
                    holdFund[0]))
            fund = json.loads(f.content)
            if not (fund['result']['data']['data'][0]['fbrq'].split(" ")[0] == str(date.today())):
                flag = 1
                break
            fundData = fund['result']['data']['data'][0]
            earningPercent = (float(fundData['jjjz']) * 100 - float(holdFund[1]) * 100) / float(holdFund[1])
            fundName = holdFund[2]
            text = text + "{}:{}%\n".format(fundName, round(earningPercent, 2))

        if flag == 1:
            print("基金尚未更新!")
            times += 1
            time.sleep(60 * 30)
    if text:
        smtp = smtplib.SMTP()
        smtp.connect(senderIMAP, 25)
        smtp.login(senderEmailAddress, senderAuthCode)
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = '{} <{}>'.format(senderEmailAddress, senderEmailAddress)
        msg['To'] = receiverEmailAddress
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        smtp.sendmail(senderEmailAddress, receiverEmailAddress, msg.as_string())
        smtp.quit()
        print("今日日报发送结束!")
    else:
        print("今日休市!")
