# @Time    : 2017/7/13 20:53
# @Author  : lileilei
# @File    : db_create.py
"""创建数据库"""
from app import db
from app.models import  Role
from config import roles


def create_roles():  # 创建角色
    """
    创建三个角色，分别是用户，
    普通管理员，超级管理员
    :return:
    :return:
    """

    roleslist=[]
    for item in roles:
        role = Role.query.filter_by(name=item).first()
        if role is None:
            role = Role(name=item)
        role.permissions = roles[item]
        roleslist.append(role)
    db.session.add_all(roleslist)
    db.session.commit()


# if __name__ == '__main__':
    # create_roles()  默认给数据库创建几个角色
    # db.create_all()
