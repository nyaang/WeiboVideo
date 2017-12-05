import requests,sys,re,time,os,json,random
from bs4 import BeautifulSoup
from getcookies import Getcookies
from values import fakeHead,fakeTail,categorys,USER_AGENTS
cookies={}
try:
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
except FileNotFoundError:
    Getcookies()
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
for cookie in json.load(cookiefile)["cookies"]:
    cookies[cookie["name"]] = cookie["value"]
cookiefile.close()

class weibovideolinks:
    def __init__(self):
        self.url=''
        self.links= {"links": set()}    #初始化links
        self.category=''
        self.page=0
        self.totalnum=0
        self.end_id=''
        self.headers={"User-Agent":''}
    def get_links_first_request(self,url,category):
        self.page = 2
        self.url=url
        self.category=category
        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        r = requests.get(self.url,cookies=cookies,headers=self.headers)
        self.bsObj=BeautifulSoup(r.content,'lxml')
        links_tag=self.bsObj.findAll("a",{"target":"_blank"})
        links_num = 0
        #统计当前请求页有多少个视频链接
        for link_tag in links_tag:
            links_num=links_num+1
            #获取href子标签，子标签中有九位字母构成的视频id
            link_href=link_tag.get('href')
            href = ''.join(re.findall('[A-Za-z0-9]{9}', link_href)[0])
            self.links["links"].add("http://weibo.com/tv/v/" + href)
        print("requested from "+self.url+" ,linksnum:"+str(links_num))
        self.totalnum=self.totalnum+links_num
        self.end_id=links_tag[links_num-1]['mid']
        '''出错了。有两种情况：
        请用浏览器打开weibo.com。
        1.显示414错误。这是请求过于频繁导致的。等几分钟就好了。
        2.未显示414错误。你的cookies.json无效。删除旧的cookies.json重新获取cookies即可。
        '''
        while(self.page<=12):
            self.getlinks()
            time.sleep(1)
            self.page=self.page+1
    def getlinks(self):
        self.url = 'https://weibo.com/p/aj/v6/mblog/videolist?type=' + self.category + '&page=' + str(
self.page) + '&end_id=' + str(self.end_id) + '&__rnd=' + str(self.generate_rnd())
        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        try:
            r = requests.get(self.url, cookies=cookies, headers=self.headers)
        except requests.exceptions.ConnectionError:
            print("链接无响应，十秒后自动重试")
            time.sleep(10)
            r = requests.get(self.url, cookies=cookies, headers=self.headers)
        links_num = 0
        data = r.json()["data"]
        data = fakeHead + str(data) + fakeTail
        self.bsObj = BeautifulSoup(data, 'html.parser')
        links_tag = self.bsObj.findAll("a", {"target": "_blank"})
        # 统计当前请求页有多少个视频链接
        for link_tag in links_tag:
            links_num = links_num + 1
            # 获取href子标签，子标签中有九位字母构成的视频id
            link_href = link_tag.get('href')
            href = ''.join(re.findall('[A-Za-z0-9]{9}', link_href)[0])
            self.links["links"].add("http://weibo.com/tv/v/" + href)
        print("requested from " + self.url + " ,linksnum:" + str(links_num))
        self.totalnum = self.totalnum + links_num
        self.end_id = links_tag[links_num - 1]['mid']
    def close(self):
        # 把视频链接写入links.json
        linkfile = open('links.json', 'w', encoding='utf-8')
        self.links["links"] = list(self.links["links"])
        json.dump(self.links, linkfile, indent=4, sort_keys=False, ensure_ascii=False)
        linkfile.close()
        print("totalnum of links:"+str(self.totalnum))
    def generate_rnd(self):
        return str(int(time.time() * 1000))
weibovlink=weibovideolinks()
for category in categorys:
    url="https://weibo.com/tv/"+category
    weibovlink.get_links_first_request(url,category)
weibovlink.close()