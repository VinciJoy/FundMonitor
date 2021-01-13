import json
import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *
from pathlib import Path

def fundMonitor():
    print("基金监控启动成功!")
    flag = 1
    times = 0
    cachePath = Path("./cache")
    today = None
    if not cachePath.exists():
        with open(cachePath, "w") as f:
            f.write("1970-1-1")

    with open(cachePath, "r") as f:
        lastDate = f.read()

    print("上次获取基金时间：{}".format(lastDate))

    while flag == 1 and times < 6:
        text = ''
        flag = 0
        for holdFund in fundList:
            try:
                f = requests.get(
                    'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol={}'.format(
                        holdFund[0]))
            except Exception as e:
                print("获取基金数据失败：{}".format(e))
                time.sleep(60 * 5)
                flag = 1
                times -= 1
                break
            fund = json.loads(f.content)
            if fund['result']['data']['data'][0]['fbrq'] == lastDate:
                flag = 1
                break
            today = fund['result']['data']['data'][0]['fbrq']
            fundData = fund['result']['data']['data'][0]
            earningPercent = (float(fundData['jjjz']) * 100 - float(holdFund[1]) * 100) / float(holdFund[1])
            fundName = holdFund[2]
            text = text + "{}:{}%\n".format(fundName, round(earningPercent, 2))

        if flag == 1:
            print("今日基金尚未更新!")
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
        with open(cachePath, "w") as f:
            f.write(today)
        print("今日日报发送结束!")
    else:
        print("今日休市!")
