MAINTAINER leizi
MAINTAINER leileili126@163.com
FROM centos
RUN yum -y update && yum -y install epel-release && yum -y install redis

EXPOSE 6379

#安装清理缓存文件
RUN yum clean all

#修改绑定IP地址
RUN sed -i -e 's@bind 127.0.0.1@bind 0.0.0.0@g' /etc/redis.conf
ENTRYPOINT [ "/usr/bin/redis-server","/etc/redis.conf"]
CMD []
COPY . /home/fxtest
RUN set -ex \
    # 预安装所需组件
    && yum install -y wget tar libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make initscripts \
    && wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz \
    && tar -zxvf Python-3.5.0.tgz \
    && cd Python-3.5.0 \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean \
    && rm -rf /Python-3.5.0* \
    && yum install -y epel-release \
    && yum install -y python-pip
# 设置默认为python3
RUN set -ex \
    # 备份旧版本python
    && mv /usr/bin/python /usr/bin/python27 \
    && mv /usr/bin/pip /usr/bin/pip-python2.7 \
    # 配置默认为python3
    && ln -s /usr/local/python3/bin/python3.5 /usr/bin/python \
    && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
# 修复因修改python版本导致yum失效问题
RUN set -ex \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down \
    && yum install -y deltarpm
# 基础环境配置
RUN set -ex \
    # 修改系统时区为东八区
    && rm -rf /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum install -y vim \
    # 安装定时任务组件
    && yum -y install cronie
# 支持中文
RUN yum install kde-l10n-Chinese -y
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 更新pip版本
RUN pip install --upgrade pip
RUN pip install  -r /home/fxtest/requirements.txt
RUN pip install uwsgi
ENV LC_ALL zh_CN.UTF-8

ADD nginx-1.19.10.tar.gz /usr/local/src

RUN yum install -y gcc gcc-c++ glibc make autoconf openssl openssl-devel
RUN yum install -y libxslt-devel -y gd gd-devel GeoIP GeoIP-devel pcre pcre-devel
RUN useradd -M -s /sbin/nologin nginx

WORKDIR /usr/local/src/nginx
CMD  ["uwsgi  -/home/fxtest/flaskapi_uwsgi.ini"]
CMD ["nginx -f /home/fxtest/flaskapi.conf"]
EXPOSE 8089
