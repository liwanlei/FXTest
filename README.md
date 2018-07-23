# IAPTest测试平台
### flask + Python3  实现的的API自动化测试平台（http协议接口、dubbo协议接口，json格式参数，）
### mocksever目前可以部分支持xml，
### 接口测试查询数据库，目前只支持mysql数据库查询。

----------------
# 敬告各位：本处代码开源后，版权仍然归属本人所有，禁止利用本项目作为出去面试，后果自负。
----------------

# 体验服地址：http://47.104.199.225

### flask +gevent+nginx+Gunicorn+supervisor部署flask应用请用flaskapi_su.conf，用gunicorn部署应用，因为在使用uwsgi部署会影响定时任务的执行
### supervisor配置可见super.conf文件。
### 钉钉群发送多用例测试任务的执行情况的时候，需要在config.py里面进行配置钉钉群自定义机器人webhook，目前体验服没有钉钉配置
### 定时任务模块定时任务测试完毕会按照config.py设置的钉钉群自定义机器人的配置进行发送通知的，当定时任务完成后，配置钉钉群会默认接受到一条钉钉机器人消息，显示定时任务的完成情况。

 ----------------
 
## v3.3版本更新日志
###  利用resetful api 思想优化代码，实现前后端分离。

## [其他版本更新日志](https://github.com/liwanlei/FXTest/blob/master/versions.md)
# 有问题可以联系我：QQ:952943386 email:leileili126@163.com  qq群：194704520  python测试开发群：683894834
#   flask部署相关文章：![Alt text](http://www.cnblogs.com/leiziv5/p/7137277.html)
#                     ![Alt text](http://www.cnblogs.com/leiziv5/p/8807135.html)                    
# 友情推荐本人其他开源代码：
#      1.python app自动化测试平台版本：![Alt text](https://github.com/liwanlei/UFATestPlan)
#      2.python+flask 做后台，实现微信小程序：![Alt text](https://github.com/liwanlei/webchat_app)
#      3.python接口测试非平台版本![Alt text](https://github.com/liwanlei/FXTest)
# 微信打赏
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/weixin.png)
 ----------------
##    效果图如下：
### 目录：
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/项目目录.png)

### 新目录：
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/最新优化后项目结构.png)


### 效果图：
#### 用户登录
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/denglu.png)
#### 首页
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/首页.png)
#### 项目界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E9%A1%B9%E7%9B%AE.png)
#### 测试环境界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/v3.0ceshihuanj.png)
#### 模块界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E8%8E%AB%E5%B0%85.png)
#### 接口界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/接口.png)
#### 接口参数界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E6%8E%A5%E5%8F%A3%E5%8F%82%E6%95%B0%E8%AF%A6%E6%83%85.png)
#### 接口参数添加界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E6%B7%BB%E5%8A%A0%E6%8E%A5%E5%8F%A3%E5%8F%82%E6%95%B0.png)
#### 接口参数编辑界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E7%BC%96%E8%BE%91%E6%8E%A5%E5%8F%A3%E5%8F%82%E6%95%B0.png)
#### 测试用例界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B.png)
#### 定时任务界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/v3.0dingshi.png)
#### 定时任务编辑界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/v3.0dingshirenbianji%20.png)
#### mockserver界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/v3.0macok.png)
#### mockserver调试界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/mocktiaposhj0.png)
#### mockserver添加界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/v3.0zengjia.png)
#### 测试报告界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A.png)
#### 用户管理界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86.png)
#### 用户设置默认邮件界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E9%82%AE%E4%BB%B6%E8%AE%BE%E7%BD%AE.png)
#### 测试报告下载后html格式的报告
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/ceshibaogao.png)
#### 测试日志
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/log.png)
