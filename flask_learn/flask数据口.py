# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/15 11:42
# software: PyCharm

"""
文件说明：
    
"""
# flask 数据库
# pip install flask-sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config:
    '''配置参数'''
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@172.0.0.1:3306/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)

# SQLAlchemy 和 app 绑定起来
db = SQLAlchemy(app)


# 创建数据库模型类
class Role(db.Model):
    '''
    角色表
    '''
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)


class User(db.Model):
    '''
    用户表
    '''
    __tablename = 'user'

    id = db.Column(db.Integer, primary_key=True)  # 默认设置自增长
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    # 表关系       外键ForeignKey，用来关联到另外一张表
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


if __name__ == '__main__':
    # 清楚所有表
    db.drop_all()
    # 创建所有的表
    db.create_all()

    # 创建对象 插入数据
    role1 = Role(name='admin')
    # session 记录到对象任务中
    db.session.add(role1)
    # 提交任务
    db.session.commit()

    # 创建对象 插入数据
    role2 = Role(name='admin2')
    # session 记录到对象任务中
    db.session.add(role2)
    # 提交任务
    db.session.commit()

    use1 = User(name='zhangsan', password='123', role_id=role1.id)
    use2 = User(name='lisi', password='321', role_id=role1.id)
    use3 = User(name='wangwu', password='321', role_id=role2.id)
    db.session.add_all([use1, use2, use3])
    db.session.commit()