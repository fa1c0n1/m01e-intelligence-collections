# m01e-intelligence-collections

简介：自动收集自己想要的情报

#### 已完成的功能如下：

1、监控github上的CVE漏洞相关的代码库，并自动将信息通过TelegramBot推送。

```
# 永久在Linux后台执行
nohup python3 github/get_poc_exp.py >/dev/null 2>&1  &
```
![image](img/github2telegrambot.png)
