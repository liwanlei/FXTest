# -*- coding: utf-8 -*-
# @Date    : 2017-07-16 18:19:45
# @Author  : lileilei
from app.models import User,Interface,InterfaceTest,db
from app import  db
for i in range(100):
    new=Interface(project_name='test'+str(i))
    new.models_name=str(i)
    new.Interface_name='测试'+(str(i))
    new.Interface_url='http://www.baid'+'i'+'.com'
    new.Interface_meth='GET'
    new.Interface_par={'ces',i}
    new.Interface_back={'code':200}
    new.Interface_user_id=1
    db.seesion.add(new)
db.seesion.commit()