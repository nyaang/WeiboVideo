# 依赖环境
请安装python3、google chrome
## **1.安装依赖**

    pip install -r requirements.txt

## **2.编辑users.py**
在ACCOUNT=和PASSWORD=的单引号中分别填入你的微博账号、密码
## **3.安装mongodb和robomongo**
可参考这篇文章：[Win10 MongoDB安装][1]
**安装成功并启动mongodb后，在浏览器中输入http://localhost:27017/,可观察到:**
> It looks like you are trying to access MongoDB over HTTP on the native driver port.

## **4.运行scrapy**

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

    


# 程序运行说明
## 获取cookie.json、links.json
 1. web_driver.py中，第六行webdriver.Chrome括号后，请修改为你本地chromedriver.exe所在的绝对路径
 2. 运行`scrapy crawl weibotv`，并登陆成功后，WeiboVideo目录下将出现cookies.json，请复制一份到weibo子目录。此时weibo子目录有如下文件（夾）
d-----        chromedriver
d-----        spiders
-a----        items.py
-a----        middlewares.py
-a----        pipelines.py
-a----        settings.py
-a----        cookies.json
 3. 运行`scrapy crawl links`，此时目录下多出links.json，此文件为视频地址池。
## 开启mongodb
**安装成功并启动mongodb后，在浏览器中输入http://localhost:27017/,可观察到:**
> It looks like you are trying to access MongoDB over HTTP on the native driver port.
## 抓取数据
 1. 得到cookies.json、links.json后，并且开启mongodb后，再次运行`scrapy crawl weibotv`，程序将从Links的视频池中选取地址抓取相应的数据并保存到数据库中。
 2. 使用robomongo新建一个connection，端口填默认的27017，如下图
![robomongo1][3]
 3. 可以看到可视化的数据
![此处输入图片的描述][4]


  [1]: http://www.jianshu.com/p/d6c7adfe45cf
  [2]: https://www.jetbrains.com/pycharm/download/#section=windows
  [3]: ./imgs/robomongo1.JPG
  [4]: ./imgs/weiboitem1..JPG