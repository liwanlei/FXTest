# FXTest测试平台
### Flask + Python3.6 +Bootstarp+Apscheduler+Sqlite+Redis 实现的接口自动化测试平台。
###  下面有介绍python flask部署相关的文章链接。为自己部署的记录文章
### 前后端部分页面开始进行分离，通过接口进行交互

----------------
##  友情提示各位：开源项目，长期不定时的维护，仅供大家参考学习使用。谢绝作为面试、毕业作品等源码。
##  后续会基于python3.6+版本去维护平台。平台所有文章都位于doc目录，或者本文章有介绍，暂无其他资料。

----------------
## 本地调试 安装依赖包后， python manage.py run即可  成功可以访问http://127.0.0.1:5000/index项目使用的数据库是sqlite
## 配置文件都在config.py，可以根据自己的实际情况进行修改

### flask +gevent+nginx+Gunicorn+supervisor部署flask应用请用flaskapi_su.conf，用gunicorn部署应用。
### supervisor配置可见super.conf文件。
### 多用例定时任务完成的通知通过的钉钉群机器人通知，没有配置会获取config.py默认的
### 定时任务现在依赖与redis做持久化，如果有报redis错误，请安装redis服务。

 ----------------
 
## 开发中功能
### 1.集成到jenkins ,目前代码需要jenkins，因此在运行的时候 需要安装jenkins
### 2.测试用例代码抽离(参考开源的接口测试框架),形成测试执行平台，用例执行的分离。
### 3.一键将接口测试用例转化为压测脚本，进行压测。转换为Jmeter脚本(后端接口开发完成)
### 4.测试用例可以依赖通用参数配置。
### 5.数据库进行调整优化，适配新功能落地。(完成)
### 6.增加黑名单功能（增加黑名单后，测试用例不在执行黑名单接口测试用例）
### 7.监控测试用例，冒烟测试用例，回归测试用例标记
### 8.倒入charles测试用例

## [其他版本更新日志](https://github.com/liwanlei/FXTest/blob/master/versions.md)
# 有问题可以联系我，增加定制开发。QQ&微信:952943386  java 版本的平台暂无开源计划。
# Email:leileili126@163.com  qq群：194704520  python接口测试：651392041 请入群人员正确回答问题。

# 个人公众号，持续更新系列文章。欢迎你关注
![Alt text](https://github.com/liwanlei/jiekou-python3/blob/master/img/weixin.png) 
#   flask部署相关文章：http://www.cnblogs.com/leiziv5/p/7137277.html
#                     http://www.cnblogs.com/leiziv5/p/8807135.html
# 友情推荐本人其他开源代码：
##      1.python app自动化测试平台版本：https://github.com/liwanlei/UFATestPlan
##      2.python+adb app性能获取小工具：https://github.com/liwanlei/python_tk_adb
##      3.python接口测试非平台版本：https://github.com/liwanlei/jiekou-python3
##      4.java开发自动化测试平台：https://github.com/liwanlei/plan
##      5.python +appium实现 UI自动化：https://github.com/liwanlei/appium-python3 已经适配stf jenkins等。 
##  开源不易，如果感觉平台对你有帮助，可以进行微信打赏
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
