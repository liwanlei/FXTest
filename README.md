# FXTest 接口自动化测试平台

> Flask + Python 3 + Bootstrap + APScheduler + Redis + SQLite/MySQL 实现的接口自动化测试平台。

----------------

## 项目简介

FXTest 是一套完整的接口自动化测试解决方案，支持：

- **接口管理**：项目管理、模块管理、接口 CRUD、接口参数配置
- **测试用例**：用例创建、多用例组合执行、用例导入导出（Excel）
- **定时任务**：基于 APScheduler + Redis 持久化，支持定时执行测试用例
- **Mock 服务**：内置 Mock Server，支持 headers/params 校验、JSON/XML 返回
- **测试报告**：HTML 格式报告自动生成，支持邮件 + 钉钉群通知
- **压测支持**：一键将接口用例转化为 JMeter JMX 脚本并远程执行
- **用户权限**：多角色权限管理（普通用户 / 管理员 / 超级管理员）
- **Flask-Admin**：后台管理系统

----------------

## 项目结构

```
FXTest/
├── app/                        # Flask 应用主目录
│   ├── case/                   # 测试用例管理 (创建/执行/导出)
│   ├── home/                   # 首页、项目、仪表盘
│   ├── interface/              # 接口管理
│   ├── mock/                   # Mock Server
│   ├── task/                   # 定时任务管理
│   ├── test_case/              # 测试执行引擎
│   ├── users/                  # 用户管理
│   ├── static/                 # 静态资源 (CSS/JS/字体/图片)
│   ├── templates/              # Jinja2 模板
│   │   ├── home/               # 主页面模板
│   │   ├── add/                # 添加表单模板
│   │   └── edit/               # 编辑表单模板
│   ├── upload/                 # 上传文件存储
│   ├── models.py               # 数据模型 (SQLAlchemy)
│   ├── forms.py                # WTForms 表单
│   ├── views.py                # 根路由视图
│   └── urls.py                 # 根路由注册
├── common/                     # 公共工具模块
│   ├── api_client.py           # HTTP API 请求封装
│   ├── assertions.py           # 断言判断
│   ├── jmx_builder.py          # JMeter JMX 脚本生成
│   ├── dingtalk.py             # 钉钉群机器人通知
│   ├── redis_client.py         # Redis 操作封装
│   ├── mysql_client.py         # MySQL 操作封装
│   ├── excel_utils.py          # Excel 写入
│   ├── excel_parser.py         # Excel 解析读取
│   ├── mock_server.py          # Mock Server 核心逻辑
│   ├── dict_utils.py           # 字典工具 (比较/解析)
│   ├── nested_dict.py          # 嵌套字典取值
│   ├── list_utils.py           # 列表合并/分页工具
│   ├── list_paging.py          # 列表分页
│   ├── pagination.py           # 分页类
│   ├── ssh_tools.py            # SSH 远程执行
│   ├── jenkins_client.py       # Jenkins API 封装
│   ├── send_email.py           # 邮件发送
│   ├── systemlog.py            # 系统日志
│   ├── test_log.py             # 测试日志
│   ├── case_logger.py          # 用例日志 (loguru)
│   ├── decorators.py           # 权限装饰器
│   ├── jsontools.py            # JSON 响应封装
│   ├── merge.py                # 字典合并
│   ├── PackageRequest.py       # HTTP 请求核心
│   └── BSTestRunner.py         # 测试执行器 (基于 unittest)
├── config.py                   # 配置文件 (环境变量 + Flask 配置)
├── manage.py                   # 应用入口
├── error_message.py            # 错误码 / 消息枚举
├── db_create.py                # 数据库初始化
├── db_migrate.py               # 数据库迁移
├── requirements.txt            # Python 依赖
├── Dockerfile                  # Docker 镜像构建
├── .env                        # 环境变量配置模板
└── .gitignore                  # Git 忽略规则
```

----------------

## 快速开始

### 1. 环境要求

- Python 3.6+
- Redis（定时任务持久化依赖）
- SQLite（默认）或 MySQL
- Jenkins（可选，Jenkins 集成代码默认已注释）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env` 为实际配置文件并按需修改：

```bash
cp .env .env
```

编辑 `.env` 填入真实值：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Flask 密钥 | - |
| `DATABASE_URL` | 数据库连接（留空使用 SQLite） | - |
| `REDIS_HOST` / `REDIS_PORT` | Redis 连接 | 127.0.0.1:6379 |
| `REDIS_PASSWORD` | Redis 密码 | 空 |
| `MAIL_USERNAME` / `MAIL_PASSWORD` | 邮件账号 | 空 |
| `DINGTALK_ACCESS_TOKEN` | 钉钉机器人 Token | 空 |
| `JENKINS_URL` / `JENKINS_USER` | Jenkins（可选） | localhost:8080 |

> 更多配置项见 `config.py` 和 `.env` 文件。

### 4. 启动应用

```bash
python manage.py
```

访问：`http://127.0.0.1:5000/index`

----------------

## 升级记录

### v4.x (当前)

- ✅ 代码安全加固：`eval()` 替换为 `ast.literal_eval()` / `json.loads()`
- ✅ 密钥管理：所有敏感配置迁移至 `.env` 环境变量
- ✅ 目录规范化：`app/Interface/` → `app/interface/`，统一小写命名
- ✅ 文件重命名：18 个 common/ 模块名从拼写错误/驼峰改为 `lowercase_underscore`
- ✅ 错误处理：修复空 `except:` → `except Exception:`，统一返回值格式
- ✅ 跨平台：`os.system('touch')` → `open(file, 'a').close()`
- ✅ 日志升级：调试 `print()` 替换为 `logger` 结构化日志
- ✅ 模板命名规范化

### v3.x

- ✅ 集成到 Jenkins
- ✅ 测试用例执行引擎重构（基于 unittest）
- ✅ 接口用例→JMeter JMX 脚本一键转化
- ✅ 通用参数配置支持
- ✅ 数据库结构优化
- ✅ 黑名单功能
- ✅ 冒烟/回归用例标记
- ✅ 日志框架升级（loguru）

[更多版本日志](https://github.com/liwanlei/FXTest/blob/master/versions.md)

----------------

## 部署

### Docker

```bash
docker build -t fxtest .
docker run -p 5000:5000 -p 6379:6379 fxtest
```

### Supervisor + Gunicorn + Nginx

参考 `flaskapi_su.conf` 配置 supervisor，`super.conf` 配置 gunicorn。

```bash
gunicorn -c super.conf manage:app
```

----------------

## 联系 & 贡献

- 邮箱：leileili126@163.com
- QQ/微信：952943386
- QQ 群：194704520
- Python 接口测试群：651392041

> 开源项目，长期不定时维护，仅供学习参考。

### 友情推荐

| 项目 | 链接 |
|------|------|
| Python App 自动化测试平台 | [UFATestPlan](https://github.com/liwanlei/UFATestPlan) |
| Python+ADB App 性能工具 | [python_tk_adb](https://github.com/liwanlei/python_tk_adb) |
| Python 接口测试（非平台版） | [jiekou-python3](https://github.com/liwanlei/jiekou-python3) |
| Java 自动化测试平台 | [plan](https://github.com/liwanlei/plan) |
| Appium Python UI 自动化 | [appium-python3](https://github.com/liwanlei/appium-python3) |

----------------

## 效果图

#### 首页
![首页](https://github.com/liwanlei/FXTest/blob/master/image/%E9%A6%96%E9%A1%B5.png)

#### 项目管理
![项目](https://github.com/liwanlei/FXTest/blob/master/image/%E9%A1%B9%E7%9B%AE.png)

#### 接口管理
![接口](https://github.com/liwanlei/FXTest/blob/master/image/%E6%8E%A5%E5%8F%A3.png)

#### 测试用例
![测试用例](https://github.com/liwanlei/FXTest/blob/master/image/%E6%B5%8B%E8%AF%95%E7%94%A8%E4%BE%8B.png)

#### 定时任务
![定时任务](https://github.com/liwanlei/FXTest/blob/master/image/v3.0dingshi.png)

#### Mock Server
![MockServer](https://github.com/liwanlei/FXTest/blob/master/image/v3.0macok.png)

#### 测试报告
![测试报告](https://github.com/liwanlei/FXTest/blob/master/image/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A.png)

#### 用户管理
![用户管理](https://github.com/liwanlei/FXTest/blob/master/image/%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86.png)