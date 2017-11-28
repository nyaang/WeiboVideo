import requests,sys,re,time,os,json
from bs4 import BeautifulSoup
from getcookies import Getcookies
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
    def __init__(self,url):
        self.url=url
        self.links= {"links": set()}    #初始化links
    def get_links(self):
        r = requests.get(self.url,cookies=cookies)
        self.bsObj=BeautifulSoup(r.content,'lxml')
        links_tag=self.bsObj.findAll("a",{"target":"_blank"})
        links_num = 0

        #统计当前请求页有多少个视频链接
        for link_tag in links_tag:
            links_num=links_num+1
            #获取href子标签，子标签中有九位字母构成的视频id
            link_href=link_tag.get('href')
            href = ''.join(re.findall('[A-Za-z0-9]{9}', link_href)[-1])
            self.links["links"].add("http://weibo.com/tv/v/" + href)
        print(links_num)
        end_id=links_tag[links_num-1]['mid']



        self.url='https://weibo.com/p/aj/v6/mblog/videolist?type='+'vfun'+'&page='+str(2)+'&end_id='+str(end_id)+'&__rnd='+str(self.generate_rnd())
        r = requests.get(self.url,cookies=cookies)
        links_num = 0
        fakeHead = """
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta charset="utf-8">
        <title>Fake Title</title>
        <body>
        """
        fakeTail = """
        </body>
        </head>
        </html>
        """
        data = r.json()["data"]
        data = fakeHead + str(data) + fakeTail
        self.bsObj=BeautifulSoup(data,'html.parser')
        links_tag=self.bsObj.findAll("a",{"target":"_blank"})
        #统计当前请求页有多少个视频链接
        for link_tag in links_tag:
            links_num=links_num+1
            #获取href子标签，子标签中有九位字母构成的视频id
            link_href=link_tag.get('href')
            href = ''.join(re.findall('[A-Za-z0-9]{9}', link_href)[-1])
            self.links["links"].add("http://weibo.com/tv/v/" + href)
        print(links_num)
        end_id = links_tag[links_num - 1]['mid']
        print(end_id)
    def close(self):
        # 把视频链接写入links.json
        linkfile = open('links.json', 'w', encoding='utf-8')
        self.links["links"] = list(self.links["links"])
        json.dump(self.links, linkfile, indent=4, sort_keys=False, ensure_ascii=False)
        linkfile.close()
    def generate_rnd(self):
        return str(int(time.time() * 1000))

weibovfun1=weibovideolinks("https://weibo.com/tv/vfun")
weibovfun1.get_links()
weibovfun1.close()