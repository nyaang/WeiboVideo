import jieba.analyse
import time
from database_utils import ConnectDB
from values import DATABASE_TV, COLLECTION_ITEM, DATE_FORMAT, REMOVE_CHAR


class ExtractTags:
    client = None
    database = None
    collection = None

    def __init__(self):
        self.client = ConnectDB(DATABASE_TV, COLLECTION_ITEM)
        self.database, self.collection = self.client.get_handler()
        jieba.enable_parallel(5)

    def remove_duplicate(self):
        all, find, delete= 0, 0, 0
        a = self.collection.distinct('url')
        for i in range(self.collection.count(),0,-1):
            all += 1
            url = self.collection.find()[i-1]["url"]
            if url in a:
                a.remove(url)
                find += 1
            elif url not in a:
                self.collection.remove(self.collection.find()[i-1])
                delete += 1
            print("Unique:%d\t\tDelete:%d\t\tProcess:%d\t\t" % (find, delete, all))

    def remove_items(self):
        items = self.collection.find({"$where": "this.comments.length  < 50" })
        for item in items:
            self.database.get_collection('remove_items').insert({"url" : item["url"]})
            self.collection.remove({"url":item["url"]})

    def cut_comments(self):
        var = 0
        for item in self.collection.find():
            comments = ""
            tags = []
            for comment in item["comments"]:
                try:
                    comments += str(comment["comment_content"])
                except TypeError:
                    break
            for char in REMOVE_CHAR:
                comments = comments.replace(char, "")
            # cut_a = '/'.join(jieba.cut_for_search(comments)) # search engine mode
            cut_a = '/'.join(jieba.cut(comments, cut_all=False)) # accurate mode
            # cut_a = '/'.join(jieba.cut(comments, cut_all=True)) # full mode
            self.collection.update({"url": item["url"]}, {"$unset": {"comments": ""}})
            self.collection.update({"url": item["url"]}, {"$set": {"comments": cut_a}})
            text_rank = jieba.analyse.textrank(cut_a, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
            for tag in text_rank:
                tags.append({"tag": tag[0], "weight": tag[1]})
            self.collection.update({"url":item["url"]}, {"$set":{"tags":tags}})
            value = time.localtime(int(time.time()))
            dt = time.strftime(DATE_FORMAT, value)
            var += 1
            print("%s\t\tprocess %d" % (dt, var))

    def close(self):
        self.client.close()

pro = ExtractTags()
pro.remove_duplicate()
pro.remove_items()
pro.cut_comments()
pro.close()