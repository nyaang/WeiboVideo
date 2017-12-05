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

#user_agent池
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]