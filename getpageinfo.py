import requests,re,time,json,pymongo,threading,random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
cookies=[]
ua = UserAgent()
proxies=json.load(open("values/proxies_useable.json", 'r', encoding='utf-8'))
links = json.load(open("values/links/links1.json", 'r', encoding='utf-8'))
class wbvpageinfo(threading.Thread):
    def __init__(self,links):
        threading.Thread.__init__(self)
        self.links=links
    def run(self):
        for link in self.links:
            self.url=link
            if (self.prasevideo() == 404):
                continue
    def getrequest(self,url):
        #使用随机的user-agent
        self.headers["User-Agent"] = ua.random
        try:
            self.cookies=random.choice(cookies)
            r = requests.get(url, cookies=self.cookies, headers=self.headers,proxies=random.choice(proxies),timeout=3.05)
            if(r.status_code==414):
                print("414错误！")
                #time.sleep(60)
                r = self.getrequest(url)
            print("requested from:" + url)
            return r
        except:
            r = self.getrequest(url)
            return r
    def decodejson(self,r):
        try:
            data=r.json()
            return data
        except json.decoder.JSONDecodeError:
            print('error')
            print(self.cookies) #账号被微博封的情况
    def prasevideo(self):
        self.comments_num=0 #评论数
        self.forwards_num=0 #转发数
        self.likes_num=0 #点赞数
        self.author='' #作者
        self.id='' #视频的16位id
        self.content='' #视频标题
        self.comments=[]
        self.forwards=[]
        self.likes=[]
        self.headers={"User-Agent":''}
        r = self.getrequest(self.url)
        self.bsObj=BeautifulSoup(r.content,'lxml')
        try:
            self.comments_num = int(
                self.bsObj.find("em", {"class": "W_ficon ficon_repeat S_ficon"}).next_sibling.get_text())
        except ValueError:
            self.comments_num=0
        except AttributeError:
            print(self.url+" 404错误，原视频页面不存在")
            return

        try:
            self.forwards_num = int(
                self.bsObj.find("em", {"class": "W_ficon ficon_forward S_ficon"}).next_sibling.get_text())
        except ValueError:
            self.forwards_num = 0

        try:
            self.likes_num = int(
                self.bsObj.find("em", {"class": "W_ficon ficon_praised S_txt2"}).next_sibling.get_text())
        except ValueError:
            self.likes_num=0

        id_tag=self.bsObj.find("a",{"class":"WB_cardmore S_txt1 S_line1 clearfix"}).get('action-data')
        try:
            self.id=re.findall('\d{16}',id_tag)[0]
        except IndexError:
            print(self.url+"链接失效")
            return 404

        self.author=self.bsObj.find("span",{"class":"W_f14 L_autocut bot_name W_fl"}).get_text()

        self.content=self.bsObj.find("div",{"class":"info_txt W_f14"}).get_text()
        self.praseforwards()
    def praseforwards(self):
        #第一次获取转发页面请求
        firsturl="http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id="+self.id+"&__rnd="+str(self.generate_rnd())
        r = self.getrequest(firsturl)
        data = self.decodejson(r)
        totalpage=data["data"]["page"]["totalpage"] #转发页面的总页数
        html = data["data"]["html"]
        self.bsObj = BeautifulSoup(html, 'html.parser')
        maxid_tag=self.bsObj.find("a",{"class":"page S_txt1 S_bg2"})
        try:
            maxid=re.findall('\d{16}',str(maxid_tag))[1]
            page = 1
            while (page <= totalpage):
                url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=' + self.id + '&max_id=' + maxid + '&page=' + str(
                    page) + '&__rnd=' + str(self.generate_rnd())
                page = page + 1
                r=self.getrequest(url)
                data = self.decodejson(r)
                html = data["data"]["html"]
                self.bsObj = BeautifulSoup(html, 'html.parser')
                #usercard_tags = self.bsObj.findAll("a", {"node-type": "name"})
                usercard_tags = self.bsObj.findAll("a", {"node-type": "feed_list_item_date"})
                for usercard_tag in usercard_tags:
                    usercard = usercard_tag.get('href')
                    try:
                        user_card = re.findall('\d{10}', usercard)[0]
                        time = re.findall("\d{1,2}月.*", usercard_tag.get_text())[0]  # 转发时间
                    except IndexError:
                        continue  # 该用户的id不是10位数字，跳过这位用户
                    self.forwards.append({
                    "forward_usercard": user_card,
                        "forward_time": time
                    })
        except IndexError:  #转发页面只有1页的情况
            self.bsObj = BeautifulSoup(html, 'html.parser')
            #usercard_tags = self.bsObj.findAll("a", {"node-type": "name"})
            usercard_tags = self.bsObj.findAll("a", {"node-type": "feed_list_item_date"})
            for usercard_tag in usercard_tags:
                usercard = usercard_tag.get('href')
                try:
                    user_card = re.findall('\d{10}', usercard)[0]
                    time = re.findall("\d{1,2}月.*", usercard_tag.get_text())[0]  # 转发时间
                except IndexError:
                    continue  # 该用户的id不是10位数字，跳过这位用户
                self.forwards.append({
                    "forward_usercard": user_card,
                    "forward_time": time
                })
        self.prasecomments()
    def get_comments(self,r):  #解析json中的评论
        data = self.decodejson(r)
        html = data["data"]["html"]
        self.bsObj = BeautifulSoup(html, 'html.parser')
        comment_tags = self.bsObj.findAll("div", {"class": "list_li S_line1 clearfix"})
        for comment_tag in comment_tags:
            comment_id = comment_tag.get('comment_id')
            comment_content_tag=comment_tag.find("div", {"class": "WB_text"})
            comment_usercard_tag = comment_content_tag.a
            try:
                comment_usercard = re.findall('\d{10}', comment_usercard_tag.get('usercard'))[0]
            except IndexError:
                continue  # 该用户的id不是10位数字，跳过这位用户

            comment_content=''
            for content in comment_content_tag:
                if (isinstance(content, str)):
                    if content=='\n' or content=='：':#过滤掉'：'和'\n'
                        continue
                    comment_content=comment_content+content
            if comment_content=='' or comment_content==' ':#如果是没有文字内容的回复，则跳过
                continue

            try:
                comment_likes_tag = comment_tag.find("em",
                                                     {"class": "W_ficon ficon_praised S_txt2"}).next_sibling.get_text()
            except AttributeError:
                comment_likes_tag = comment_tag.find("em", {
                    "class": "W_ficon ficon_praised S_txt2"}).next_sibling.next_sibling.get_text()

            if comment_likes_tag == '赞':  # 此时视频的点赞数为0
                comment_likes = 0
            else:
                comment_likes = int(comment_likes_tag)
            comment_time = re.findall("\d{1,2}月.*", comment_tag.get_text())[0]  #评论时间
            self.comments.append({"comment_content": comment_content,
                                  "comment_id": comment_id,
                                  "comment_likes": comment_likes,
                                  "comment_usercard": comment_usercard,
                                  "comment_time": comment_time
                                  })
    def get_comments_way2_more_comments(self,r):  #解析json中的评论，增加一次判断去重，用于二级评论的第一次加载
        data = self.decodejson(r)
        html = data["data"]["html"]
        self.bsObj = BeautifulSoup(html, 'html.parser')
        comment_tags = self.bsObj.findAll("div", {"class": "list_li S_line1 clearfix"})
        for comment_tag in comment_tags:
            comment_id = comment_tag.get('comment_id')
            comment_content_tag=comment_tag.find("div", {"class": "WB_text"})
            comment_usercard_tag = comment_content_tag.a
            try:
                comment_usercard = re.findall('\d{10}', comment_usercard_tag.get('usercard'))[0]
            except IndexError:
                continue  # 该用户的id不是10位数字，跳过这位用户

            comment_content=''
            for content in comment_content_tag:
                if (isinstance(content, str)):
                    if content=='\n' or content=='：':#过滤掉'：'和'\n'
                        continue
                    comment_content=comment_content+content
            if comment_content=='' or comment_content==' ':#如果是没有文字内容的回复，则跳过
                continue

            try:
                comment_likes_tag = comment_tag.find("em",
                                                     {"class": "W_ficon ficon_praised S_txt2"}).next_sibling.get_text()
            except AttributeError:
                comment_likes_tag = comment_tag.find("em", {
                    "class": "W_ficon ficon_praised S_txt2"}).next_sibling.next_sibling.get_text()

            if comment_likes_tag == '赞':  # 此时视频的点赞数为0
                comment_likes = 0
            else:
                comment_likes = int(comment_likes_tag)

            bool_exist=False
            for comment in self.comments:   #如果评论已在评论列表中，则不再次添加
                if comment_id == comment["comment_id"]:
                    bool_exist = True
                    continue
            if bool_exist == False:
                self.comments.append({"comment_content": comment_content,
                                      "comment_id": comment_id,
                                      "comment_likes": comment_likes,
                                      "comment_usercard": comment_usercard})
    def loadmorepage(self):
        try:
            nextpage = self.bsObj.find("div", {"node-type": "comment_loading"}).get("action-data")
            return nextpage
        except AttributeError:
            try:
                nextpage = self.bsObj.find("a", {"action-type": "click_more_comment"}).get("action-data")
                return nextpage
            except AttributeError:
                return False
    def load_more_comment(self,bsObj):
        try:
            more_comment_tags=self.bsObj.findAll("a",{"action-type":"click_more_child_comment_big"})
            for more_comment_tag in more_comment_tags:
                more_comment_tag=more_comment_tag.get("action-data")
                more_comment_url='https://weibo.com/aj/v6/comment/big?ajwvr=6&'+more_comment_tag+'&from=singleWeiBo&__rnd='+str(self.generate_rnd())
                r=self.getrequest(more_comment_url)
                self.get_comments_way2_more_comments(r)
                self.load_more_comment_continue()
            self.bsObj=bsObj
        except AttributeError:  #没有二级评论
            return
    def load_more_comment_continue(self):
        try:
            more_comment_tag = self.bsObj.find("a", {"action-type": "click_more_child_comment_big"}).get("action-data")
            more_comment_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&' + more_comment_tag + '&from=singleWeiBo&__rnd=' + str(
                self.generate_rnd())
            r = self.getrequest(more_comment_url)
            self.get_comments(r)
            self.load_more_comment_continue()
        except AttributeError:
            return
    def get_comments_way2(self):
        firsturl='https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+self.id+'&filter=all&from=singleWeiBo&__rnd='+str(self.generate_rnd())
        r = self.getrequest(firsturl)
        self.get_comments(r)

        while self.loadmorepage()!=False:
            url='https://weibo.com/aj/v6/comment/big?ajwvr=6&'+self.loadmorepage()
            r = self.getrequest(url)
            self.get_comments(r)
            self.load_more_comment(self.bsObj)
    def prasecomments(self):
        #第一次获取评论请求
        firsturl='https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+self.id+'&page=1'+"&__rnd="+str(self.generate_rnd())
        r=self.getrequest(firsturl)
        data = self.decodejson(r)
        try:
            totalpage = data["data"]["page"]["totalpage"]
            page = 1
            while (page <= totalpage):  # 常规方式获取评论
                url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=' + self.id + '&page=' + str(
                    page) + "&__rnd=" + str(self.generate_rnd())
                r = self.getrequest(url)
                self.get_comments(r)
                page = page + 1
        except KeyError:
            self.get_comments_way2()    #用第二种方式获取评论
        self.updatedb()
    def generate_rnd(self):
        return str(int(time.time() * 1000))

    def updatedb(self):
        client=pymongo.MongoClient('127.0.0.1:27017')
        db=client['WeiboTV']
        db['WeiboItem'].insert(
            {"author": self.author,
             "content": self.content,
             "id": self.id,
             "url": re.findall('[A-Za-z0-9]{9}',self.url)[0],
             "comments_num": self.comments_num,
             "likes_num": self.likes_num,
             "forwards_num": self.forwards_num,
             "comments": self.comments,
             "forwards": self.forwards, #pymongo.errors.ServerSelectionTimeoutError: No servers found yet
             }
        )
def opencookies(cookiename):
    try:
        cookiefile = open('values/'+cookiename+'.json', 'r', encoding='utf-8')
    except FileNotFoundError:
        return False
    cookiename={}
    for cookie in json.load(cookiefile)["cookies"]:
        cookiename[cookie["name"]] = cookie["value"]
    cookiefile.close()
    cookies.append(cookiename)
    return True
def start(threadnum):
    i = 1
    while opencookies('cookies' + str(i)):
        i = i + 1
    linksqueue=[]
    links_len = len(links)
    split_num = links_len // threadnum
    i = 1
    while (i < threadnum):
        linki=links[split_num * (i-1):split_num * i]
        linksqueue.append(wbvpageinfo(linki))
        i = i + 1
    linkend=links[split_num * (i-1):links_len]
    linksqueue.append(wbvpageinfo(linkend))
    i = 0
    while (i < threadnum):
        linksqueue[i].start()
        i=i+1
start(1)  #在此输入进程数

