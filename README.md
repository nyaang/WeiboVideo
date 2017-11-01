**依赖环境：python3、google chrome**

**1.安装依赖**

    pip install -r requirements.txt

**2.编辑users.py，在ACCOUNT=和PASSWORD=的单引号中分别填入你的微博账号、密码**


**3.安装mongodb和robomongo**
可参考这篇文章：[Win10 MongoDB安装][1]
安装成功并启动mongodb后，在浏览器中输入http://localhost:27017/ ,可观察到:
> It looks like you are trying to access MongoDB over HTTP on the native driver port.

**4.运行scrapy**

进入weibo目录，打开命令行，
 

    `scrapy crawl weibotv`  ，程序将运行spiders目录下的wbtv.py
    `scrapy crawl links`  ，程序将运行spiders目录下的links
    `scrapy crawl relation`  ，程序将运行spiders目录下的relation.py


  [1]: http://www.jianshu.com/p/d6c7adfe45cf
  
