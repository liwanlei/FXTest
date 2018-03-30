# IAPTest测试平台
### flask + Python3  实现的的API自动化测试平台（http接口，json格式参数）
### mocksever目前可以部分支持xml，
### 接口测试查询数据库，目前只支持mysql数据库查询。

----------------

### 注：钉钉群发送多用例测试任务的执行情况的时候，需要在config.py里面进行配置钉钉群自定义机器人webhook
### 定时任务模块定时任务测试完毕会按照config.py设置的钉钉群自定义机器人的配置进行发送通知的，当定时任务完成后，配置钉钉群会默认接受到一条钉钉机器人消息，显示定时任务的完成情况。

 ----------------
 
# dubbo分支(本分支还未进行相应的调试，bug可能比较多)
### 1.开发针对dubbo接口的支持
###  2.修复优化部门脚本。
###  3.对现有bug进行修复
###  4.对现有的结构进行了部分的优化
# v3.1.1版本

### 1.mockserver模块的优化，对部分前后端代码进行调整，
### 2.修复部分已知bug
### 3.暂时去掉导入测试用例和接口测试模块。
### 4.优化部分代码，增加对404界面和500界面的处理。
### 5.增加后台管理模块，只有管理员才能进入后台管理，用户管理中心， 非管理员在前端界面是不展示的两个入口

# v3.1.0版本

### 1.单个接口增加依赖单个接口
### 2.单个接口，多个接口可以保存测试结果
### 3.多个用例测试依赖单个接口
### 4.增加多个用例测试的时候测试结果情况分类，异常，参数等错误个数也能进行收集。
### 5.测试报告可以根据项目进行选择展示，选择不同的项目展示不同项目下面的测试报告。
### 6.接口展示根据项目展示，并且这里会根据你的权限展示项目。ajax请求获取的测试接口。去掉了之前版本的搜索功能。
### 7.接口测试用例，可以根据项目选择，项目有权限控制在里面。ajax异步加载获取测试接口测试用例。去掉了之前版本的搜索功能。
### 8.测试环境追加测试数据库，可以在后面的测试用例中查询数据库，进行断言。
### 9.测试用例可以选择增加查询数据库，进行数据库取值比较，校验接口的正确性。

# quanxianbanben 

###  增加优化权限功能，对用户权限进行划分，用户登录系统后会根据自己的权限去看到对应的内容。根据自己的权限可以有相应的操作。
### 本版本对项目结构进行了进一步优化，将case，Interface等地方功能形成单独的app注册到主app中，进行结构拆分重组，讲文档并入doc的目录中，对已知bug进行修复。

# v3.0.2功能：

### 1.增加单个用例对测试环境区分的测试，单个用例可以分别选择该用例所属项目的测试环境进行测试。测试环境区分不仅仅在用例执行，也可以在部署后的主机手动修改hosts来改变测试环境。

 # v3.0.1功能：
 
 ### 1.定时任务完成后，通知改成了钉钉群机器人发送测试通知，配置在config文件进行配置，申请群机器人的详细可以参考钉钉开发文档。
 ### 2.多任务模块代码优化，可以选择钉钉群机器人通知结果，或者选择默认邮箱发送测试报告，优化整合多用例执行。对部分代码进行优化重构
 
 #  v3.0功能：
 
 ### 1.增加定时任务，定时任务定时执行，执行完毕发送测试报告，目前定时任务没有持久化。容易受到宕机的原因影响，需要每次重启重新启动。
 ### 2.增加测试环境，目前可自由去添加测试环境，没有增加测试用例的时候选择测试环境
 ### 3.mockserver功能的开发，可以使用这个进行mock功能，开启后点击路径就可以访问mock
 
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
###   1.用户注册，
###   2.用户登录，
###   3.首页，统计平台的用例、测试报告、接口的统计，提供模板下载，这里的下载的接口模板和测试用例的模板下载后，可以在Excel中写好后，直接导入我们的测试平台。
###   4接口界面，可以添加接口，编辑接口，删除，可以去批量导入，模板在首页接口模板下载，可以通过项目，模板进行测试用例的搜索。
###   5.用例界面。 可以在界面添加测试用例，可以去批量导入，用例有变动的时候，可以去编辑下用例，用例输入错误，可以去删除测试用例，可以进行用例的搜索，单个的用例可以单独执行，批量执行的测试用例会单独生成测试报告，在测试报告界面可以下载，看结果
###   6.测试报告，展示批量执行的测试用例，可以去下载测试日志，和测试报告，
###   7。用户管理。 可以查询用户，添加用户，冻结用户，取消管理，重置密码。非管理员不能进入这个界面。

# 有问题可以联系我：QQ:952943386 email:leileili126@163.com  qq群：194704520  新群：683894834
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
#### 模块界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/%E8%8E%AB%E5%B0%85.png)
#### 接口界面
![Alt text](https://github.com/liwanlei/FXTest/blob/master/image/接口.png)
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
