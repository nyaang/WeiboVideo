import requests
import pymongo
import threading
import json
import random
from fake_useragent import UserAgent

userids = json.load(open("userids.json", 'r', encoding='utf-8'))
ua = UserAgent()


class wbrelation(threading.Thread):
    def __init__(self, userids):
        threading.Thread.__init__(self)
        self.userids = userids

    def run(self):
        for userid in self.userids:
            self.userid = userid
            self.getuser()

    def getrequest(self, url):
        self.headers = {"User-Agent": ''}
        self.headers["User-Agent"] = ua.random
        try:
            r = requests.get(url, headers=self.headers)
            if (r.status_code == 414):
                print("60错误！")
                r = self.getrequest(url)
            print("requested from:" + url)
            return r
        except requests.exceptions.ConnectionError:
            print("连接无响应，重试")
            r = self.getrequest(url)
            return r
        except requests.exceptions.ChunkedEncodingError:
            r = self.getrequest(url)
            return r

    def decodejson(self, r):
        try:
            data = r.json()
            if (data["ok"] == 1):
                return data
            elif (data["ok"] == 0 and data["msg"] != '这里还没有内容'):
                print("ip暂时被封")
                r = self.getrequest(r.url)
                data = self.decodejson(r)
                return data
        except json.decoder.JSONDecodeError as e:
            print(e)
            if(e == 'Extra data: line 1 column 75 (char 74)'):  # 用户不存在
                return None
            elif(e == 'Expecting value: line 1 column 1 (char 0)'):  # 网络不好
                print("网络不好")
                r = self.getrequest(r.url)
                data = self.decodejson(r)
                return data

    def getuser(self):
        self.guanzhu = 0
        self.fensi = 0
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s' % self.userid
        r = self.getrequest(url)
        data = self.decodejson(r)
        try:
            self.guanzhu = data["data"]["userInfo"]["follow_count"]
        except KeyError:
            return
        except TypeError:
            return
        self.fensi = data["data"]["userInfo"]["followers_count"]
        print(self.guanzhu)
        print(self.fensi)
        self.getfollow()

    def getfollow(self):
        self.followuser_id = []
        num = int(self.guanzhu / 20)
        if self.guanzhu % 20 == 0:
            num = num - 1
        if num >= 10:
            num = 9
        for page in range(1, num + 2):
            try:
                url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_%s&luicode=10000011&lfid=1005051259110474&page=%d" % (
                    self.userid, page)
                self.follow_num = 0
                self.fans_num = 0
                r = self.getrequest(url)
                data = self.decodejson(r)
                try:
                    user1 = data["data"]["cards"][0]
                except IndexError:
                    continue
                except KeyError:
                    continue
                except TypeError:
                    continue
                for i in range(0, 20):
                    try:
                        userid = user1["card_group"][i]
                        userii = userid["user"]
                        user_id = userii["id"]
                        hh = len(str(user_id))
                        if (int(hh > 10)):
                            i = i + 1
                        else:
                            self.followuser_id.append(str(user_id))
                    except IndexError:
                        continue
            except KeyError:
                continue
            print('爬取完成')
        self.getfans()

    def getfans(self):
        self.fansuser_id = []
        num = int(self.fensi / 20)
        if self.fensi % 20 == 0:
            num = num - 1
        if num > 250:
            num = 249
        for page in range(1, num + 2):
            url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_%s&type=all&since_id=%d" % (
                self.userid, page)
            self.headers = {"User-Agent": ""}
            self.follow_num = 0
            self.fans_num = 0
            self.headers["User-Agent"] = ua.random
            r = self.getrequest(url)
            data = self.decodejson(r)
            try:
                user1 = data["data"]["cards"][0]
            except IndexError:
                continue
            except KeyError:
                continue
            except TypeError:
                continue
            for i in range(0, 20):
                try:
                    userid = user1["card_group"][i]
                    userii = userid["user"]
                    user_id = userii["id"]
                    self.fansuser_id.append(str(user_id))
                except IndexError:
                    continue
                except KeyError:
                    continue
            print('爬取完成')
        self.updatedb(self.userid)

    def updatedb(self, nowuser):
        client = pymongo.MongoClient('127.0.0.1:27017')
        db = client['WeiboTV']
        db['Relation'].insert(
            {"source_id": nowuser,
             "follow": self.followuser_id,
             "fans": self.fansuser_id
             }
        )
        userids.remove(self.userid)
        self.updateuserids()

    def updateuserids(self):
        userfile = open('usersnew.json', 'w', encoding='utf-8')
        json.dump(
            userids,
            userfile,
            indent=4,
            sort_keys=False,
            ensure_ascii=False)
        userfile.close()


def start(threadnum):
    linksqueue = []
    links_len = len(userids)
    split_num = links_len // threadnum
    i = 1
    while (i < threadnum):
        linki = userids[split_num * (i - 1):split_num * i]
        linksqueue.append(wbrelation(linki))
        i = i + 1
    linkend = userids[split_num * (i - 1):links_len]
    linksqueue.append(wbrelation(linkend))
    i = 0
    while (i < threadnum):
        linksqueue[i].start()
        i = i + 1


start(2)
