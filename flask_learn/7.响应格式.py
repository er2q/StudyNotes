# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/14 23:10
# software: PyCharm

"""
文件说明：
    
"""
from flask import Flask, make_response, json, jsonify

app = Flask(__name__)
# 直接返回json
app.config['JSON_AS_ASCII'] = False


@app.route('/index')
def index():
    data = {
        'name': '张三'
    }
    # return make_response(json.dumps(data, ensure_ascii=False))
    # 返回前端为json格式
    # response = make_response(json.dumps(data, ensure_ascii=False))
    # response.mimetype = 'application/json'
    # return response
    # 直接返回json
    return jsonify(data)


if __name__ == '__main__':
    app.run()
