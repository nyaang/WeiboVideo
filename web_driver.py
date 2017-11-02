import time
import json
from selenium import webdriver
from users import ACCOUNT, PASSWORD

class GetCookies:
    def __init__(self):
        self.driver = webdriver.Chrome('./weibo/chromedriver/chromedriver.exe') #相对路径调用weibo/chrome/下的chromedriver
        #self.driver.maximize_window()
        self.driver.get('http://weibo.com/login.php') #跳转微博首页
        time.sleep(3)
        self.run()

    def run(self):
        try:
            self.driver.find_element_by_xpath('//div[@class="info_list username"]/div/input').send_keys(ACCOUNT)    #找到用户名的输入框，自动输入用户名
            print('input username')
        except:
            print('username error!')
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('//div[@class="info_list password"]/div/input').send_keys(PASSWORD)   #自动输入密码
            print('input password')
        except:
            print('password error!')
        time.sleep(10)   #暂停十秒，如遇到验证码，请在十秒内输入
        try:
            self.driver.find_element_by_xpath('//div[@class="info_list login_btn"]/a').click()  #自动点击登录按钮
            print('click to login')
        except:
            print('click error!')
        time.sleep(10)
        cookies={"cookies":[]}
        for item in self.driver.get_cookies():  #获取cookies，并写入本地，命名为cookies.json
            cookies["cookies"].append({"name":item["name"], "value":item["value"]})
        cookies["cookies"]=list(cookies["cookies"])
        file = open('cookies.json', 'w', encoding='utf-8')
        json.dump(cookies, file, indent=4, sort_keys=False, ensure_ascii=False)
        file.close()
        self.driver.close()

