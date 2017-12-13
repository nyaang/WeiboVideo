import requests,re,time,json,random
from bs4 import BeautifulSoup
from getcookies import Getcookies
from values import USER_AGENTS
cookies={}
try:
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
except FileNotFoundError:
    Getcookies()
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
for cookie in json.load(cookiefile)["cookies"]:
    cookies[cookie["name"]] = cookie["value"]
cookiefile.close()

class wbvpageinfo():
    def __init__(self,url):
        self.comments_num=0 #评论数
        self.forwards_num=0 #转发数
        self.likes_num=0 #点赞数
        self.author='' #作者
        self.id='' #视频的16位id
        self.url=url #视频的9位url
        self.content='' #视频标题
        self.comments=[]
        self.forwards=[]
        self.likes=[]
        self.headers={"User-Agent":''}
    def prasevideo(self):
        #使用随机的user-agent
        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        try:
            r = requests.get(self.url, cookies=cookies, headers=self.headers)
        except requests.exceptions.ConnectionError:
            print("连接无响应，3秒后自动重试")
            time.sleep(3)
            r = requests.get(self.url, cookies=cookies, headers=self.headers)
        print("requested from:"+self.url)
        self.bsObj=BeautifulSoup(r.content,'lxml')

        self.comments_num = int(
            self.bsObj.find("em", {"class": "W_ficon ficon_repeat S_ficon"}).next_sibling.get_text())
        self.forwards_num = int(
            self.bsObj.find("em", {"class": "W_ficon ficon_forward S_ficon"}).next_sibling.get_text())
        self.likes_num = int(
            self.bsObj.find("em", {"class": "W_ficon ficon_praised S_txt2"}).next_sibling.get_text())

        id_tag=self.bsObj.find("a",{"class":"WB_cardmore S_txt1 S_line1 clearfix"}).get('action-data')
        self.id=re.findall('\d{16}',id_tag)[0]

        self.author=self.bsObj.find("span",{"class":"W_f14 L_autocut bot_name W_fl"}).get_text()

        self.content=self.bsObj.find("div",{"class":"info_txt W_f14"}).get_text()
    def praseforwards(self):

        #第一次获取转发页面请求
        firsturl="http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id="+self.id+"&__rnd="+str(self.generate_rnd())
        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        try:
            r = requests.get(firsturl, cookies=cookies, headers=self.headers)
        except requests.exceptions.ConnectionError:
            print("连接无响应，3秒后自动重试")
            time.sleep(3)
            r = requests.get(firsturl, cookies=cookies, headers=self.headers)
        print("requested from:"+firsturl)
        data = r.json()
        totalpage=data["data"]["page"]["totalpage"] #转发页面的总页数
        html = data["data"]["html"]
        self.bsObj = BeautifulSoup(html, 'html.parser')
        maxid_tag=self.bsObj.find("a",{"class":"page S_txt1 S_bg2"})
        maxid=re.findall('\d{16}',str(maxid_tag))[1]

        page=1
        while(page<=totalpage):
            url='https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id='+self.id+'&max_id='+maxid+'&page='+str(page)+'&__rnd='+str(self.generate_rnd())
            page=page+1
            try:
                r = requests.get(url, cookies=cookies, headers=self.headers)
            except requests.exceptions.ConnectionError:
                print("连接无响应，3秒后自动重试")
                time.sleep(3)
                r = requests.get(url, cookies=cookies, headers=self.headers)
            print("requested from:" + url)
            data = r.json()
            html=data["data"]["html"]
            self.bsObj = BeautifulSoup(html, 'html.parser')
            usercard_tags = self.bsObj.findAll("a",{"node-type":"name"})

            for usecard_tag in usercard_tags:
                usercard=usecard_tag.get('usercard')
                user_card=re.findall('\d{10}',usercard)[0]
                tempusercard = {'forward_usercard': ''}  # 字典临时变量
                tempusercard['forward_usercard']=user_card
                self.forwards.append(tempusercard)
        # cardfile = open('usercards.json', 'w', encoding='utf-8')
        # json.dump(self.forwards, cardfile, indent=4, sort_keys=False, ensure_ascii=False)
        # cardfile.close()
    def generate_rnd(self):
        return str(int(time.time() * 1000))
    #def prasecomments(self):
wbvpage=wbvpageinfo("https://weibo.com/tv/v/FxUgH9Xq9")
wbvpage.prasevideo()
wbvpage.praseforwards()