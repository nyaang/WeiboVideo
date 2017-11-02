# 依赖环境
请安装python3、google chrome
## **1.安装依赖**

    pip install -r requirements.txt


## **2.安装mongodb和robomongo**
可参考这篇文章：[Win10 MongoDB安装][1]
**安装成功并启动mongodb后，在浏览器中输入http://localhost:27017/,可观察到:**
> It looks like you are trying to access MongoDB over HTTP on the native driver port.

## **3.运行scrapy**

进入weibo目录，打开命令行，
 

    `scrapy crawl weibotv`  ，程序将运行spiders目录下的wbtv.py
    `scrapy crawl links`  ，程序将运行spiders目录下的links.py
    `scrapy crawl relation`  ，程序将运行spiders目录下的relation.py
# 程序调试说明
以[JetBrains PyCharm Community Edition 2017.2.3][2]为例。
**main.py文件中**，
对应内容分别为
 1. `cmdline.execute("scrapy crawl weibotv".split())`此时为从wbtv.py开始调试
 2. `cmdline.execute("scrapy crawl links".split())`此时为从links.py开始调试
 3. `cmdline.execute("scrapy crawl relation".split())`此时为从links.py开始调试
以调试wbtv.py为例。
在wbtv中设置断点后，在pycharm中**debug执行main.py**,即可开始断点运行。断点运行后可开始单步调试。
未获取cookies.json时，wbtv会调用web_driver.py文件，所以在web_driver.py中设置断点后，debug执行main.py同样可以断点调试或者单步调试web_driver.py文件。

**同样的，按1、2、3分别修改main.py后，debug main.py时能分别对wbtv.py、links.py、relation.py及其调用的其他.py文件进行调试。**

    


  [1]: http://www.jianshu.com/p/d6c7adfe45cf
  [2]: https://www.jetbrains.com/pycharm/download/#section=windows