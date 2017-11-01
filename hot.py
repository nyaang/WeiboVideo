from pymongo import MongoClient

client = MongoClient('127.0.0.1:27017')
database = client.get_database('WeiboTV')
collection = database.get_collection('WeiboItem')

sum_comments = 0
sum_forwards = 0
videos = {}
for item in collection.find():
    try:
        forwards = len(item["forwards"])
    except KeyError:
        forwards = 0
    try:
        comments = len(item["comments"])
    except KeyError:
        comments = 0
    videos[item["url"]] = len(item["forwards"]) + len(item["comments"])
sort = sorted(videos.items(), key = lambda x: x[1], reverse=True)
top20 = []
for i in range(20):
    (u, v) = sort[i]
    top20.append(u)
print(top20)
