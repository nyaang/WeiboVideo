import requests,re,time,json,random,pymongo,threading
from getcookies import Getcookies
from values import USER_AGENTS
from lxml import etree
cookies={}
import json
#https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474 个人信息
#https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)  #微博个人首页
#https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474&containerid=2302831259110474&page=1
#https://m.weibo.cn/p/index?containerid=231051_-_fansrecomm_-_1259110474&luicode=10000011&lfid=1005051259110474
#https://m.weibo.cn/api/container/getIndex?containerid=2304131259110474_-_WEIBO_SECOND_PROFILE_WEIBO&luicode=10000011&lfid=2302831259110474&page_type=03&page=1 #微博内容



try:
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
except FileNotFoundError:
    Getcookies()
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
for cookie in json.load(cookiefile)["cookies"]:
    cookies[cookie["name"]] = cookie["value"]
cookiefile.close()
class wbrelation():

    def getrequest(self,url):
        #使用随机的user-agent
        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        try:
            r = requests.get(url, cookies=cookies, headers=self.headers)
            if r.content ==b'':
                print("网络错误")
                time.sleep(20)
                r = self.getrequest(url)
            if(r.status_code==414):
                print("60错误！")
                time.sleep(120)
                r = self.getrequest(url)
            print("requested from:" + url)
            return r
        except requests.exceptions.ConnectionError:
            print("连接无响应，1秒后自动重试")
            time.sleep(1)
            r = self.getrequest(url)
            return r

    def get_containerid(self,url):
        self.headers = {"User-Agent": ""}
        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        nowuser = '5019697368'
        url="https://m.weibo.cn/api/container/getIndex?type=uid&value=%s" %(nowuser)
        r = self.getrequest(url)
        content = json.loads(r)
        for data in content.get('tabsInfo').get('tabs'):
            if (data.get('tab_type') == 'weibo'):
                containerid = data.get('containerid')
                print(containerid)
        return containerid

    def getuser(self,nowuser):
        self.guanzhu=0
        self.fensi=0
        self.headers = {"User-Agent": ""}

        self.headers["User-Agent"] = (random.choice(USER_AGENTS))
        #nowuser = '1259110474'
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s'%(nowuser)
        print(url)
        r = self.getrequest(url)

        data = r.json()
        self.guanzhu = data["data"]["userInfo"]["follow_count"]
        self.fensi= data["data"]["userInfo"]["followers_count"]
        print(self.guanzhu)
        print(self.fensi)
        #description = content.get('userInfo').get('description')
        #profile_url = content.get('userInfo').get('profile_url')
        #self.guanzhu = user1['follow_count']     #关注数
        #self.name = content.get('userInfo').get('screen_name')          #昵称
        #self.fensi = user1['followers_count']    #粉丝数
        #gender = content.get('userInfo').get('gender')
        #urank = content.get('userInfo').get('urank')



    def getfollow(self,nowuser):
        self.followuser_id=[]
        num = int(self.guanzhu/20)
        if self.guanzhu%20==0:
            num=num-1
        if num>=10:
            num=9
        for page in range(1,num+2):
          #nowuser='1259110474'
          try:
              url="https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_%s&luicode=10000011&lfid=1005051259110474&page=%d"%(nowuser,page)
              self.headers = {"User-Agent": ""}
              self.follow_num = 0
              self.fans_num = 0
              self.headers["User-Agent"] = (random.choice(USER_AGENTS))
              r = self.getrequest(url)
              # r=requests.get(url,cookies=cookies,headers=self.headers).content
              try:
                 data=r.json()
              except json.decoder.JSONDecodeError:
                  break
              #print(data)
              try:
                 user1=data["data"]["cards"][0]
              except IndexError:
                continue
              for i in range (0,20):
               try:
                 userid=user1["card_group"][i]
                 userii=userid["user"]
                 user_id=userii["id"]
                 hh=len(str(user_id))
                 if(int(hh>10)):
                     i=i+1
                 else:
                   user_name=userii["screen_name"]
                   self.followuser_id.append(str(user_id))
                   #users_id=user_id.strip()
                   print(str(user_id)+ ' : '+user_name)
                #print(user_name)
               except IndexError:
                   continue
          except KeyError:
              continue
        print(self.followuser_id)
    def getfans(self,nowuser):
        self.fansuser_id=[]
        num=int(self.fensi/20)
        if self.fensi%20==0:
            num=num-1
        if num>250:
            num=249
        for page in range(1,num+2):
          #nowuser='1259110474'
          url="https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_%s&type=all&since_id=%d"%(nowuser,page)
          self.headers = {"User-Agent": ""}
          self.follow_num = 0
          self.fans_num = 0
          self.headers["User-Agent"] = (random.choice(USER_AGENTS))
          r = self.getrequest(url)
          try:
              data = r.json()
          except json.decoder.JSONDecodeError:
              break
          try:
            user1=data["data"]["cards"][0]
          except IndexError:
              continue
          except KeyError:
              continue
          for i in range (0,20):
            try:
                userid=user1["card_group"][i]
                userii=userid["user"]
                user_id=userii["id"]
                user_name=userii["screen_name"]
                self.fansuser_id.append(str(user_id))
                print(str(user_id) + ' : '+user_name)
                #print(user_name)
            except IndexError:
                  continue
        print(self.fansuser_id)


    def updatedb(self,nowuser):
        #nowuser='1259110474'
        client = pymongo.MongoClient('127.0.0.1:27017')
        db = client['WeiboTV']
        db['Relation'].insert(
            {"source_id":nowuser,
             "follow":self.followuser_id,
             "fans":self.fansuser_id
             }
        )
run=wbrelation()
with open('userid.txt', 'r') as f0:
    lines = f0.readlines()
    for line in lines:

        nowuser = line.strip()
        run.getuser(nowuser)
        run.getfollow(nowuser)
        run.getfans(nowuser)
        run.updatedb(nowuser)

