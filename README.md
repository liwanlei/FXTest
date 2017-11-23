# IAPTest测试平台
### flask + Python3  实现的的API自动化测试平台（http接口，json格式参数）
 mocksever目前可以部分支持xml
 ----------------
 #  v3.0功能：
 ### 1.增加定时任务，定时任务定时执行，执行完毕发送测试报告，目前定时任务没有持久化。容易受到宕机的原因影响，需要每次重启重新启动。
 ### 2.增加测试环境，目前可自由去添加测试环境，没有增加测试用例的时候选择测试环境
 ### 3.mockserver功能的开发，可以使用这个进行mock功能，暂时支持path只有一部分
#  v2.0功能：
### 1.增加选择岗位
### 2.项目模块，功能模块只有管理员才能删除
### 3.只有管理员才能进入用户管理模块
### 4.可以选择发送邮件，必须有默认邮箱
###  5.点击右上角用户名可以去设置默认邮箱，可以设置多个邮件接受的，但是只能设置一个默认的，默认发送邮件测试报告
### 6.增加可视化的测试结果，依靠百度开源的可视化框架。地址：http://echarts.baidu.com

# v1.0功能：
### 这里主要实现的是api接口，接口测试用例，测试报告，用户管理。主要有一下功能。
## 功能：
####   1.用户注册，
####   2.用户登录，
####   3.首页，统计平台的用例、测试报告、接口的统计，提供模板下载，这里的下载的接口模板和测试用例的模板下载后，可以在Excel中写好后，直接导入我们的测试平台。
####   4接口界面，可以添加接口，编辑接口，删除，可以去批量导入，模板在首页接口模板下载，可以通过项目，模板进行测试用例的搜索。
####   5.用例界面。 可以在界面添加测试用例，可以去批量导入，用例有变动的时候，可以去编辑下用例，用例输入错误，可以去删除测试用例，可以进行用例的搜索，单个的用例可以单独执行，批量执行的测试用例会单独生成测试报告，在测试报告界面可以下载，看结果
####   6.测试报告，展示批量执行的测试用例，可以去下载测试日志，和测试报告，
####   7。用户管理。 可以查询用户，添加用户，冻结用户，取消管理，重置密码。非管理员不能进入这个界面。

# 有问题可以联系我：QQ:952943386 email:leileili126@163.com  qq群：194704520  新群：683894834
# 微信打赏
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/weixin.png)
 ----------------
##    效果图如下：
### 目录：
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/项目目录.png)

### 新目录：
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E6%96%B0%E7%9B%AE%E5%BD%95.png)

### 效果图：
#### 用户登录
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/denglu.png)
#### 用户注册
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/zhuce.png)
#### 首页
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/首页.png)
#### 项目界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E9%A1%B9%E7%9B%AE.png)
#### 模块界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E8%8E%AB%E5%B0%85.png)
#### 接口界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/接口.png)
#### 测试用例界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B.png)
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
