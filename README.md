# FundMonitor
[介绍]

该脚本可以将每日的基金收益发送到指定邮箱，打开微信的邮箱提醒服务后可以直接在微信接收到基金收益的更新。

[初始化]

使用python3.7运行

`pip install -r requirements.txt`

安装相应的环境

[配置]

只需修改config里的相应变量

[运行]

`python3.7 main.py`

[说明]

该脚本会从九点开始，每过半小时查询一次基金信息是否更新。