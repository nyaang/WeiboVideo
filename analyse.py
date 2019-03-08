from pymongo import MongoClient

DB_Name = 'WeiboTV'
Collection_Name = 'WeiboItem'
NUM = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"]


class Analyse:
    def __init__(self):
        self.client = MongoClient()
        self.database = self.client[DB_Name]
        self.collection = self.database[Collection_Name]

    def average(self):
        result = {}
        for i in range(10):
            var = 0
            total = 0
            for item in self.collection.find():
                var += len(item["relative"][NUM[i]])
                total += 1
            result[NUM[i]] = var / total
        print(result)

    def export(self, num):
        file = open('result_%s.csv' % str(num), 'w', encoding='utf-8')
        file.writelines("Source,Target,Weight,Type\n")
        temp = set()
        for item in self.collection.find():
            for url in item["relative"][NUM[num]]:
                if (url["url"], item["url"]) in temp:
                    continue
                else:
                    temp.add((item["url"], url["url"]))
                    file.writelines([item["url"], ',', url["url"], ',', str(
                        url["value"])[0:5], ',', 'undirected\n'])
        file.close()

    def count(self):
        user = {}
        for weiboitem in self.collection.find():
            for forward in weiboitem["forwards"]:
                usercard = forward["forward_usercard"]
                if user.get(usercard) is None:  # 如果转发过的用户不在user集合中，则加入user字典
                    user[usercard] = set()
                user[usercard].add(weiboitem["url"])

        active_users = self.database.get_collection('users')
        var = 0
        for (u, v) in user.items():
            if len(v) > 9:  # 如果一个用户的转发视频数大于9，则插入user数据库
                active_user_cursor = active_users.find({"usercard": u})
                if active_user_cursor.count() != 0:  # 检查该用户是否已经在数据库中
                    continue
                active_users.insert(
                    {"usercard": u}, {"$set": {"forwards": len(v)}})
            var += 1
            print(var)
        # for i in range(max+1):
        #     sum = 0
        #     p = 0
        #     for count in user.values():
        #         if count == i:
        #             sum += count
        #             p += 1
        #     file.write("forward %d:\t\tpeople:%d\n" % (i+1, p))
        # for i in range(2,max):
        #     result = {}
        #     for (u, count) in user.items():
        #         if count > i:
        #             result[u] = count
        #     print(i,":", len(result))


a = Analyse()
# a.average()
# a.export()
a.count()
