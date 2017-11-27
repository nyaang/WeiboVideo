import json
from selenium import webdriver
def Getcookies():
    chromedriver=webdriver.Chrome('./weibo/chromedriver/chromedriver.exe')
    chromedriver.get('https://weibo.com/login.php')
    tempchar=input("请在登陆完成,并且页面加载完毕后输入任意字符，输入后程序将立刻获取cookies:")   #此行用来拖时间，用于登陆
    cookies={"cookies":[]}
    for item in chromedriver.get_cookies():  #获取cookies，并写入本地，命名为cookies.json
        cookies["cookies"].append({"name":item["name"], "value":item["value"]})
    file = open('cookies.json', 'w', encoding='utf-8')
    json.dump(cookies, file, indent=4, sort_keys=False, ensure_ascii=False)
    file.close()
    chromedriver.close()
Getcookies()