import jieba.analyse
import time
from pymongo import MongoClient
DB_Name = 'WeiboTV'
Collection_Name = 'WeiboItem'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
REMOVE_CHAR = {"[", "]", "'", "回复", "："}


class ExtractTags:
    def __init__(self):
        self.client = MongoClient()
        self.database = self.client[DB_Name]
        self.collection = self.database[Collection_Name]
        # jieba.enable_parallel(5)   #parallel模式，不支持windows

    def remove_items(self):  # 去除评论数小于50的视频，放入remove_items表
        items = self.collection.find({"$where": "this.comments.length  < 50"})
        for item in items:
            self.database.get_collection('remove_items').insert_one(item)
            self.collection.remove({"url": item["url"]})

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
            cut_a = '/'.join(jieba.cut_for_search(comments)
                             )  # search engine mode
            # cut_a = '/'.join(jieba.cut(comments, cut_all=False)) # accurate mode
            # cut_a = '/'.join(jieba.cut(comments, cut_all=True)) # full mode
            self.collection.update({"url": item["url"]}, {
                                   "$unset": {"comments": ""}})
            self.collection.update({"url": item["url"]}, {
                                   "$set": {"comments": cut_a}})
            text_rank = jieba.analyse.textrank(
                cut_a, topK=20, withWeight=True, allowPOS=(
                    'ns', 'n', 'vn', 'v'))
            for tag in text_rank:
                tags.append({"tag": tag[0], "weight": tag[1]})
            self.collection.update({"url": item["url"]}, {
                                   "$set": {"tags": tags}})
            value = time.localtime(int(time.time()))
            dt = time.strftime(DATE_FORMAT, value)
            var += 1
            print("%s\t\tprocess %d" % (dt, var))

    def close(self):
        self.client.close()


pro = ExtractTags()
# pro.remove_items()
pro.cut_comments()
pro.close()
