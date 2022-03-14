# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/14 21:03
# software: PyCharm

"""
文件说明：
    
"""
# 轻量级 后端框架
# 1.flask路由  用来匹配url
# 2.request对象 abort函数
# 3.模板
# 4.flask数据库
# 5.表单
# 6.ajax
# 7.系统管理小案例
# 安装 pip install flask
from flask import Flask

# 实例化
app = Flask(__name__)

@app.route('/') # 路由
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run()