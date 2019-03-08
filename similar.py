import time,numpy,threading
from numpy import *
from copy import deepcopy
from pymongo import MongoClient

DB_Name = 'WeiboTV'
Collection_Name = 'WeiboItem'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
class Similar(threading.Thread):

    def __init__(self,items):
        threading.Thread.__init__(self)
        self.client = MongoClient()
        self.database = self.client[DB_Name]
        self.collection = self.database[Collection_Name]
        self.items=items
    def run(self):
        self.process()
    @staticmethod
    def cosine(a, b):   #求余弦
        return a.dot(b)/sqrt(a.dot(a))/sqrt(b.dot(b))

    def add_tags(self, item, tag_set):  #关键词合并
        for t in item["tags"]:
            tag_set.add(t["tag"])
        return tag_set

    def cut_split(self, item):  #以‘/’划分关键词
        comment = item["comments"]
        cut = comment.split('/')
        comment = comment.replace('/','')
        length = len(comment.replace('/',''))
        return comment, cut, length

    def init_vec(self, tags):   #初始化向量
        vec = {}
        for i in tags:
            vec[i] = 0
        return vec

    def frequence(self, cut, len, tags):    #求关键词在评论中的相对词频
        vec = self.init_vec(tags)
        for word in cut:
            if word in tags:
                vec[word] += 1.0 / len
        li = list(map(lambda x:x, vec.values()))
        ar = numpy.array(li)
        return ar

    def process(self):  #求相似度
        links = 0
        var = 0
        for item_a in self.items:
            # all = 0
            # pos = 0
            tag = self.add_tags(item_a, set())
            relative = {}
            for i in range(10):
                relative[NUM[i]] = []
            comments_a, cut_a, len_a = self.cut_split(item_a)
            for item_b in self.collection.find():
                if item_a != item_b:
                    tags = self.add_tags(item_b, deepcopy(tag))
                    comments_b, cut_b, len_b = self.cut_split(item_b)
                    vec_a = self.frequence(cut_a, len_a, tags)
                    vec_b = self.frequence(cut_b, len_b, tags)
                    cos = self.cosine(vec_a, vec_b)
                    for i in range(10):
                        if cos > 0.1 * i :
                            links += 1
                            relative[NUM[i]].append({"url":item_b["url"], "value":cos})
                            if len(relative[NUM[i]]) == 0:
                                break
            self.collection.update({"url":item_a["url"]},{"$set":{"relative":relative}})
            var += 1
            value = time.localtime(int(time.time()))
            dt = time.strftime(DATE_FORMAT, value)
            print("%s\t\tprocesse %d\t\t" % (dt, var))
def start(threadnum):
    client = MongoClient()
    database = client[DB_Name]
    collection = database[Collection_Name]
    similaritems=[]
    wbitemsqueue = []
    for wbitem in collection.find():
        wbitemsqueue.append(wbitem)

    items_len = len(wbitemsqueue)
    split_num = items_len // threadnum
    i = 1
    while (i < threadnum):
        itemsi=wbitemsqueue[split_num * (i-1):split_num * i]
        similaritems.append(Similar(itemsi))
        i = i + 1
    itemend=wbitemsqueue[split_num * (i-1):items_len]
    similaritems.append(Similar(itemend))
    i = 0
    while (i < threadnum):
        similaritems[i].start()
        i=i+1
start(24)
# pro = Similar()
# pro.process()