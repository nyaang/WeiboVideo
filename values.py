# -*- coding: utf-8 -*-
# Filename
FILENAME_COOKIES = 'cookies.json'
FILENAME_LINKS = 'links.json'

# MongDB
LOCAL_HOST = '127.0.0.1'
PORT = 27017
DATABASE_TV = 'WeiboTV'
COLLECTION_ITEM = 'WeiboItem'
COLLECTION_URL = 'WeiboUrl'

# Format
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Others
REMOVE_CHAR = {"[", "]", "'", "回复", "："}
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TOP = ['F60AinHUg', 'F5XEEAgNm', 'F5Zy5vvBV', 'F5PsSzGap', 'F5PulgouS', 'F4MxrxWtM', 'F5VZ95vsP', 'F53pYAhn4', 'F4TMpaaEe', 'F60Lj0ktx', 'F5GNAihfg', 'F5nChaFn5', 'F5vCznV11', 'F4Jqvpv2O', 'F5wbSFUDM', 'F4MXz7pQv', 'F5W2OiqfJ', 'F5PQd0AdW', 'F5QwhlobH', 'F5PoS4bR6']

# Regex
HREF_REGEX = '[A-Za-z0-9]{9}'
URL_REGEX = '/tv/v/' + HREF_REGEX
USERCARD_REGEX = '\d{10}'
MID_REGEX = '\d{16}'

# URL
URL_COMMENTS = 'http://weibo.com/aj/v6/comment/big?ajwvr=6& id=%s&root_comment_max_id=%s&root_comment_max_id_type=&root_comment_ext_param=&page=%s&filter=all& sum_comment_number=%s&filter_tips_before=0&from=singleWeiBo&__rnd=%s'
URL_OTHER_PAGE = "http://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803_ctg1_1199_-_ctg1_1199&feed_sort=102803_ctg1_11991_-_ctg1_11991&feed_filter=102803_ctg1_11991_-_ctg1_11991&pre_page=%s&page=%s&pids=Pl_Core_NewMixFeed__3&current_page=%s&since_id=&pl_name=Pl_Core_NewMixFeed__3&id=102803_ctg1_1199_-_ctg1_1199&script_uri=/102803_ctg1_1199_-_ctg1_1199&feed_type=1&domain_op=102803_ctg1_1199_-_ctg1_1199&__rnd=%s"
URL_FIRST_PAGE = "http://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803_ctg1_1199_-_ctg1_1199&feed_sort=102803_ctg1_11991_-_ctg1_11991&feed_filter=102803_ctg1_11991_-_ctg1_11991&pagebar=%s&tab=home&current_page=%s&pre_page=%s&page=%s&pl_name=Pl_Core_NewMixFeed__3&id=102803_ctg1_1199_-_ctg1_1199&script_uri=/102803_ctg1_1199_-_ctg1_1199&feed_type=1&domain_op=102803_ctg1_1199_-_ctg1_1199&__rnd=%s"

fakeHead = """
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta charset="utf-8">
        <title>Fake Title</title>
        <body>
        """
fakeTail = """
</body>
</head>
</html>
"""

#所有分类
categorys={'vfun','game','dance','music','movie','tech','discovery','lifestyle','show','world','sports','moe'}