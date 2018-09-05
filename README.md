# flashWeb_TrendAnalyze
## 各文件功能
- flaskWeb.py  
   web文件
- trendAnalyze.py  
   主程序文件
- client.py  
    客户端模拟
- test_data.xml  
    测试数据
## 本服务功能
#### 本服务包含两个功能：
1. 一个坐标轴，横坐标为12个月份，每个月份一个点，总共12个点，对这12个点判断趋势，并且找出异常点，并说明异常点对总趋势的影响
1. 一个坐标轴内，会有多条曲线（如5条），其中一条是总量曲线，还有4条是子量曲线，如何判定总量曲线的上升下降受影响因素，例如：最近作案人数曲线有所上升，常住人口作案人数上升，但是上升趋势不如总量高，暂住人口和流动人口上升趋势明显比总量高，未成年作案人数下降，那么影响总量人口上升的主要是暂住人口和流动人口，反之亦然  
#### 输入输出
- 输入：  
    - xml方式：  
        实例：  
        使用功能一
        ```xml
        <data>
            <fun>1</fun>  
            <num>3</num>
            <items>
                <item>1538,1681,1961,1741,1448,1748,1784,2036,1732,1182,1797,1744</item>  
                <item>3087,4555,7815,9705,4700,4703,5252,4709,4712,1705,4718,4721</item>  
                <item>3421,4199,3612,3569,3525,3459,3405,3347,3229,1208,4187,4155</item>  
            </items>  
        </data>  
        ```  
        使用功能二
        ```xml
        <data>
            <fun>2</fun>
            <num>5</num>
            <items>
                <item>1538,1681,1961,1741,1448,1748,1784,2036,1732,1182,1797,1744</item>
                <item>600,601,400,603,345,605,606,567,608,643,610,611</item>
                <item>400,478,893,403,343,405,406,407,408,19,410,411</item>
                <item>169,189,202,232,256,205,266,555,208,11,267,211</item>
                <item>369,413,466,503,504,533,506,507,508,509,510,511</item>
            </items>
        </data>
        ```
        > fun：使用的功能，1或2  
        > num：条目数  
        > items：条目内容  
        >> item：每条条目内容，从一月到十二月每个月的值，用英文','隔开。
    - 数据库方式: 查看```trendAnalyze.py```文件注释
- 输出：  
    功能一的输出实例
    ```xml
    <?xml version='1.0' encoding='UTF-8'?>
    <out>
        <item id="1">
            <w>
                <month>8</month>
                <value>-5.300129366106063</value>
            </w>
            <w>
                <month>10</month>
                <value>13.740532959326877</value>
            </w>
            <description>总体呈下降趋势
                因8月的影响使案件数量下降变缓
                因10月的影响使案件数量从上升趋势变为了下降趋势
            </description>
        </item>
        <item id="2">
            <w>
                <month>1</month>
                <value>-322.9818181818177</value>
            </w>
            <w>
                <month>4</month>
                <value>-81.6114819759679</value>
            </w>
            <w>
                <month>10</month>
                <value>-86.06030855539949</value>
            </w>
            <description>总体呈下降趋势
                因1月的影响使案件数量下降变缓
                主要是4月的影响使案件数量下降更明显
                主要是10月的影响使案件数量下降更明显
            </description>
        </item>
        <item id="3">
            <w>
                <month>10</month>
                <value>22.822580645161466</value>
            </w>
            <w>
                <month>11</month>
                <value>-76.31654135338353</value>
            </w>
            <w>
                <month>12</month>
                <value>-89.51818181818156</value>
            </w>
            <description>总体呈下降趋势
                因10月的影响使案件数量从上升趋势变为了下降趋势
                因11月的影响使案件数量下降变缓
                因12月的影响使案件数量下降变缓
            </description>
        </item>
    </out>
    ```  
    > item：每条曲线的内容  
    >> w：曲线斜率
    >>> month：缺少的月份  
    >>> value：斜率值  
    >> 
    >> description：描述

    功能二的输出实例
    ```xml
    <out>
        <w id="1">9.073426573426609</w>
        <w id="2">-22.346153846153825</w>
        <w id="3">2.3251748251748374</w>
        <w id="4">9.59090909090911</w>
        <w_dataSum>-1.356643356643282</w_dataSum>
        <description>总结：影响总的下降趋势的主要是"data2"</description>
    </out>
    ```
    > w：每条线的斜率值  
    > w_dataSum：总曲线斜率值  
    > descripiton：描述
## ubuntu部署方法
1. 安装python 2.7
2. 安装虚拟环境工具->安装虚拟环境->进入虚拟环境  
    ```
    1. sudo apt install virtualenv  
      
    2. virtualenv -p /usr/bin/python2 --no-site-packages py2env  
      
    3. source py2env/bin/activate
    ```
3. 进入项目目录
4. 安装依赖：
    ```
    pip install -r requirements.txt
    ```
5. 编辑 ```uconfig.ini```文件（在项目目录下创建```uconfig.ini```文件）
    ```
    [uwsgi]

    # 外部访问地址，可以指定多种协议，现在用http便于调试，之后用socket
    http = 0.0.0.0:5000
      
    # 指向项目目录
    chdir = /home/ubuntu/trendAnalyze/flashWeb_TrendAnalyze
    # flask启动程序文件
    wsgi-file = flaskWeb.py
     
    # flask在manage.py文件中的app名
    callable = app
     
    # 处理器数
    processes = 4
     
    # 线程数
    threads = 2
     
    #状态检测地址
    stats = 127.0.0.1:9191
    ```
6. 可以用 ```uwsgi uconfig.ini```命令启动uwsgi，然后就可以用外网测试(要关闭uwsgi可以kill相应进程)
7. 安装 Supervisor：```sudo apt-get install supervisor```
 
    Supervisor可以同时启动多个应用，最重要的是，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。  
    
    Supervisor 的全局的配置文件位置在：```/etc/supervisor/supervisor.conf ```
    正常情况下我们并不需要去对其作出任何的改动，只需要添加一个新的 *.conf 文件放在```/etc/supervisor/conf.d/```下
    ```
    [program:trendAnalyze]
    # 启动命令入口
    command=/home/ubuntu/virtulenvs/py2env/bin/uwsgi /home/ubuntu/trendAnalyze/flashWeb_TrendAnalyze/uconfig.ini
    # 命令程序所在目录
    dictory=/home/ubuntu/trendAnalyze/flashWeb_TrendAnalyze
    #运行命令的用户名
    user=root
      
    autostart=true
    autorestart=true
    #日志地址
    stdout_logfile=/home/ubuntu/trendAnalyze/flashWeb_TrendAnalyze/uwsgi_supervisor.log

    ```
8. 启动Supervisor  
    启动服务：```sudo service supervisor start```  
    终止服务：```sudo service supervisor stop```  
    重启服务：```sudo service supervisor restart```  
9. 安装Nginx(非必须，主要用于反向代理)：  
    ```sudo apt-get install nginx```
    Nginx是轻量级、性能强、占用资源少，能很好的处理高并发的反向代理软件。Ubuntu 上配置 Nginx 也是很简单，不要去改动默认的 nginx.conf 只需要将```/etc/nginx/sites-available/default```文件替换掉就可以了。 
    新建一个 default 文件:
    ```
    server {
        listen  5000;
        server_name 127.0.0.1; # 公网ip？
        location / {
                uwsgi_pass      127.0.0.1:8001;
                include uwsgi_params;
                uwsgi_param UWSGI_PYHOME /home/ubuntu/virtulenvs/py2env; # 指向>虚拟环境目
                uwsgi_param UWSGI_CHDIR  /home/ubuntu/trendAnalyze/flashWeb_TrendAnalyze; # 指向网站根目录
                uwsgi_param UWSGI_SCRIPT manage:app; # 指定启动程序
        }
    ```
    启动服务：
    ```
    1. sudo service supervisor start
    2. sudo service nginx start
    ```
> 参考博客[“flask项目部署到阿里云服务器”](https://blog.csdn.net/qq_16293649/article/details/78601569)
 ## Windows部署方法
1. **安装python 2.7**
2. **安装虚拟环境工具->安装虚拟环境->进入虚拟环境**  
    ```
    1. pip install virtualenv  
      
    2. virtualenv --no-site-packages py2env  
      
    3. py2env\Scripts\acticate.bat
    ```
3. **进入项目目录**
4. **安装依赖：**
    ```
    pip install -r requirements_win.txt
    ```
5. **安装Apache**  
    <font color=red>**!!!注意!!!**  
    > 如果下面这一点没有做到，整个过程有99%的可能性会失败。  
    Apache,mod_wsgi和Python都必须用相同版本的C/C++编译器生成，它们要么是32位的，要么是64位的，不能混用，同时编译方式从VC9到VC12都有，也不能混用。  </font>

    从[这里](http://www.apachelounge.com/download/ )下载相应版本Apache（版本说明看[这里](https://github.com/GrahamDumpleton/mod_wsgi/blob/master/win32/README.rst)），<font color=green>或者直接从[这里](https://zh.osdn.net/projects/sfnet_appmm/downloads/httpd-2.4.6-win32-VC9.zip/)下载httpd-win32-VC9(适用于32位python2)</font>，然后选择对应的版本，将Apache24文件夹拷贝到C:\。当然，你可以拷贝到你的系统的任何位置，但Apache的默认配置是C:\Apache24。  
    
    如果你本机运行了IIS，将其关掉。因为IIS和Apache都默认用的是80端口。如果你想配置其它端口，我相信那也不难。等把Flask部署成功后再来捣鼓吧。  
    >打开cmd  
    ```
    > cd c:\  
    > cd Apache24\bin\
    > httpd
    ```

    然后打开浏览器，输入 http://localhost  
    如果网页上显示 It Works! ，那说明apache服务器运行起来了。
6. **安装mod_wsgi**  
    从[这里](https://code.google.com/p/modwsgi/downloads/detail?name=mod_wsgi-win32-ap22py27-3.3.so)下载mod_wsgi，<font color=green>或者直接从[这里](https://github.com/GrahamDumpleton/mod_wsgi/releases/tag/4.4.12)下载</font>，然后选择相应版本的.so文件,比如```mod_wsgi-py27-VC9.so```文件，将其拷贝至C:\Apache24\modules\下，并更名为mod_wsgi.so。

    打开 c:\Apache24\conf\httpd.conf 添加如下配置  
    ```
    LoadModule wsgi_module modules/mod_wsgi.so
    ```

    重新启动httpd，如果没有报错，说明mod_wsgi模块在apache里面加载成功了。
7. **在Apache中配置站点**  
    将以下配置代码加入到C:\Apache24\conf\httpd.conf文件中
    ```
    <VirtualHost *:80 >
    ServerAdmin example@company.com
    DocumentRoot "D:\code\flashWeb_TrendAnalyze" 
    <Directory "D:\code\flashWeb_TrendAnalyze">
    Order allow,deny
    Allow from all 
    Require all granted
    </Directory>
    WSGIScriptAlias / D:\code\flashWeb_TrendAnalyze\run.wsgi
    </VirtualHost>
    ```

    重启httpd，打开浏览器，输入```http://localhost/hello```，若显示“Hello World！”，则为配置成功。
8. **安装、启动Apache服务**  
    可以在Apache安装目录的bin子目录下使用如下命令安装一个Apache服务。如果没有指定服务名称和配置文件，则在安装时使用默认服务名称Apache2.4，默认配置文件conf/httpd.conf。  
    ```
    C:\Apache2.4\bin> httpd  -k  install 
    ```
    当在同一台机器上装有多个Apache服务时，必须为它们指定不同的名称，这样方便管理。可以使用下面的命令来指定服务的名称，其中“ApacheShop”为指定的服务名称。
    ```
    C:\Apache2.4\bin> httpd  -k  install  -n  ApacheShop 
    ```
    如果想为不同的服务指定不同的配置文件，可以在安装时使用如下的命令来指定：
    ```
    C:\Apache2.4\bin> httpd  -k  install  -n  
    ApacheShop -f "C:/Apache2.4/conf/my.conf" 
    ```
    ```
    C:\Apache2.4\bin> httpd  -k  uninstall  
    ```
    也可以移除指定名称的服务，如下所示：
    ```
    C:\Apache2.4\bin> httpd  -k  uninstall  -n  ApacheShop 
    ```
    ---  
    启动Apache服务
    ```
    NET START Apache2.4
    ```
    关闭Apache服务
    ```
    NET STOP Apache2.4
    ```
    ---  
    在启动Apache服务之前，可以使用下面的命令来检查配置文件的正确性。```C:\Apache2.4\bin> httpd  -n  Apache2.4  -t ```  
    还可以通过命令行控制Apache服务。启动一个已安装的服务：```C:\Apache2.4\bin> httpd  -k  start ```  
    停止一个已安装的服务：```C:\Apache2.4\bin> httpd  -k  stop```或  ```C:\Apache2.4\bin> httpd  -k  shutdown ```  
    重新启动一个运行中的服务，可以使用下面的命令强制其重新加载配置文件：```C:\Apache2.4\bin> httpd  -k  restart ```
    

**启动完Apache服务后即可开始使用服务**  
>参考博客[Flask + mod_wsgi + Apache on Windows 部署成功(随时接受提问)](https://blog.csdn.net/firefox1/article/details/46438769)和[1.2.2 启动、停止和重新启动Apache服务（1）](http://book.51cto.com/art/201110/298017.htm)
