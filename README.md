# flashWeb_TrendAnalyze
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
5. 编辑 ```uconfig.ini```文件
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
> 参考博客[flask项目部署到阿里云服务器](https://blog.csdn.net/qq_16293649/article/details/78601569)
 ## Windows部署方法
 