import pymongo,time
client=pymongo.MongoClient()
db=client['WeiboTV']
wbitem_collection=db['WeiboItem']
wbgroup_collection = db['WeiboGroup']
def isin(cursor):
    l=0
    for item in cursor:
        l=l+1
    return l
def initgroup():
    for wbitem in wbitem_collection.find():
        cursor = wbgroup_collection.find({'url': wbitem['url']})
        if isin(cursor)==0:
            wbgroup_collection.insert(
                {'url':wbitem['url'],
                   '0':'0',
                   '1':'0',
                   '2':'0',
                   '3':'0',
                   '4':'0',
                   '5':'0',
                   '6':'0',
                   '7':'0',
                   '8':'0',
                   '9':'0'
                 }
            )
        else:
            print('already in the colletion')

def insert_into_Group(item):
    #if in WeiboGroup，then update the value of groupi
    groupi=0
    while(groupi<=9):
        try:
            groupivalue=item[str(groupi)]
            # print (str(groupi)+ ':' +str(groupivalue))
            wbgroup_collection.update_one(
                {"url": item['url']},
                {"$set":{str(groupi):str(groupivalue)}}
            )
            groupi=groupi+1
        except KeyError:
            groupi=groupi+1
            continue

def main():
    initgroup()
    for wbitem in wbitem_collection.find():
        insert_into_Group(wbitem)
main()
