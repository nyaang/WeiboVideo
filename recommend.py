from values import DATABASE_TV, COLLECTION_ITEM, NUM, TOP
from database_utils import ConnectDB
import random

PICKED = False
USERS = []
RECOMMEND_TOP = TOP

class Recommend:
    client = None
    database = None
    users_c = None
    users = None
    item_c = None
    group_c = None
    video_set = None
    similar = 0

    def __init__(self, cut='search', similar=2):
        self.client = ConnectDB(DATABASE_TV, 'users')
        self.database, self.users_c = self.client.get_handler()
        self.users = []
        self.item_c = self.database.get_collection('WeiboItem_similar_search')
        collection = 'WeiboGroup_' + cut
        self.group_c = self.database.get_collection(collection)
        self.similar = similar
        self.all_videos = []

    def pick_user(self, num=20):
        length = self.users_c.count()
        result = self.users_c.find()
        for i in range(num):
            self.users.append(result[random.randrange(length)]["usercard"])

    def pick_a_video(self, user):
        self.video_set = self.item_c.find({"forwards.forward_usercard": user})
        ran = self.video_set.count()
        return self.video_set[random.randrange(ran)]["url"]

    def get_watched(self,  user):
        watched = []
        for video in self.item_c.find({"forwards.forward_usercard":user}):
            watched.append(video["url"])
        return watched

    def get_group(self, item):
        try:
            group = item[str(self.similar)]
        except:
            if self.similar == 0:
                raise ValueError("wrong similar!")
            else:
                self.similar -= 1
                group = self.get_group(item)
        return group

    def get_videos(self, group, source):
        global ALL_VIDEOS
        temp = []
        source = self.item_c.find_one({"url":source["url"]})
        for item in self.group_c.find({str(self.similar):group}):
            temp.append(item["url"])
        all = {}
        for items in source["relative"]["zero"]:
            if items["url"] in temp:
                all[items["url"]] = items["value"]
        sort = sorted(all.items(), key=lambda item: item[1], reverse=True)
        recommend = []
        for (u,v) in sort:
            if len(recommend) > 20:
                break
            else:
                if v >= self.similar * 0.1:
                    recommend.append(u)
                else:
                    break
        recommend_random = []
        for i in range(20):
            ran = random.randint(0, len(ALL_VIDEOS) - 1)
            recommend_random.append(ALL_VIDEOS[ran])
        return recommend, recommend_random

    def process(self):
        global PICKED
        global USERS, RECOMMEND_TOP
        user_num = user_num_random = user_num_top = 30
        if not PICKED:
            self.pick_user(user_num)
            USERS = self.users
            PICKED = True
        else:
            self.users = USERS
        rate_p = 0
        rate_r = 0
        rate_p_random = 0
        rate_r_random = 0
        rate_p_top = 0
        rate_r_top = 0
        for user in self.users:
            url = self.pick_a_video(user)
            item = self.group_c.find_one({"url": url})
            group = self.get_group(item)
            recommend, recommend_random = self.get_videos(group, item)
            watched = self.get_watched(user)
            correct = 0
            correct_random = 0
            correct_top = 0
            total = len(recommend)
            total_random = len(recommend_random)
            total_top = 20
            t = len (watched)
            for video in recommend:
                if video in watched:
                    correct += 1
            try:
                rate_p += correct / total
                rate_r += correct / t
                file.write("%s\t\t%s\t\t%s\n" % (user, str(correct / total), str(correct / t)))
                print(user, correct/total, correct/t)
            except ZeroDivisionError:
                user_num -= 1
            for video in recommend_random:
                if video in watched and video != url:
                    correct_random += 1
            try:
                rate_p_random += correct_random / total_random
                rate_r_random += correct_random / t
                file.write("%s\t\t%s\t\t%s\n" % (user, str(correct_random / total_random), str(correct_random / t)))
                print(user, correct_random/total_random, correct_random/t)
            except ZeroDivisionError:
                user_num_random -= 1
            for video in RECOMMEND_TOP:
                if video in watched and video != url:
                    correct_top += 1
            try:
                rate_p_top += correct_top / total_top
                rate_r_top += correct_top / t
                file.write("%s\t\t%s\t\t%s\n" % (user, str(correct_top / total_top), str(correct_top / t)))
                print(user, correct_top/total_top, correct_top/t)
            except ZeroDivisionError:
                user_num_top -= 1
        p = rate_p/user_num
        r = rate_r/user_num
        print("======================================")
        try:
            print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 2 * p * r / (p + r)))
            file.write("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 2 * p * r / (p + r)))
        except ZeroDivisionError:
            print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 0))
            file.write("average:%lf\t\t%lf\t\tscore:%lf\n" % (p, r, 0))
        p_random = rate_p_random / user_num_random
        r_random = rate_r_random / user_num_random
        try:
            print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p_random, r, 2 * p_random * r_random / (p_random + r_random)))
            file.write("random_average:%lf\t\t%lf\t\tscore:%lf\n" % (p_random, r_random, 2 * p_random * r_random / (p_random + r_random)))
        except ZeroDivisionError:
            print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p_random, r, 0))
            file.write("random_average:%lf\t\t%lf\t\tscore:%lf\n" % (p_random, r_random, 0))
        p_top = rate_p_top / user_num_top
        r_top = rate_r_top / user_num_top
        try:
            print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p_top, r_top, 2 * p_top * r_top / (p_top + r_top)))
            file.write("top_average:%lf\t\t%lf\t\tscore:%lf\n" % (p_top, r_top, 2 * p_top * r_top / (p_top + r_top)))
        except ZeroDivisionError:
            print("average:%lf\t\t%lf\t\tscore:%lf\n" % (p_top, r_top, 0))
            file.write("top_average:%lf\t\t%lf\t\tscore:%lf\n" % (p_top, r_top, 0))

# file = open('search.txt','w')
# for i in range(10):
#     file.write("===================================================================\n")
#     pro = Recommend('search', i)
#     pro.process()
# file.close()
# file = open('full.txt','w')
# for i in range(10):
#     file.write("===================================================================\n")
#     pro = Recommend('full', i)
#     pro.process()
# file.close()
ALL_VIDEOS = []
client = ConnectDB("WeiboTV", "WeiboItem")
d, c = client.get_handler()
for item in c.find():
    ALL_VIDEOS.append(item["url"])
file = open('result.txt','w')
for i in range(500):
    file.write("\nExperiment %d\n===================================================================\n" % i)
    pro = Recommend('accurate', i)
    pro.process()
file.close()