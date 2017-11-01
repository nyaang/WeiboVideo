from database_utils import ConnectDB
from values import DATABASE_TV, COLLECTION_ITEM, NUM


class Analyse:
    client = None
    database = None
    collection = None

    def __init__(self):
        self.client = ConnectDB(DATABASE_TV, COLLECTION_ITEM)
        self.database, self.collection = self.client.get_handler()

    def average(self):
        result = {}
        for i in range(10):
            var = 0
            total = 0
            for item in self.collection.find():
                var += len(item["relative"][NUM[i]])
                total +=1
            result[NUM[i]] = var/total
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
                    temp.add((item["url"],url["url"]))
                    file.writelines([item["url"], ',', url["url"], ',', str(url["value"])[0:5], ',', 'undirected\n'])
        file.close()

    def count(self):
        user = {}
        for item in self.collection.find():
            for forward in item["forwards"]:
                usercard = forward["forward_usercard"]
                if user.get(usercard) is None:
                    user[usercard] = set()
                user[usercard].add(item["url"])

        data = self.database.get_collection('users')
        var = 0
        for (u, v) in user.items():
            if len(v) > 9:
                data.insert({"usercard":u},{"$set":{"forwards":len(v)}})
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
a.count()
