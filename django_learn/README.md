# 达内Django

`Linux` 关闭服务

```shell
sudo lsof -i:8000 # 查询出进程ID

kill -9 ID
```

## 项目结构

```shell
# tree /f
│  db.sqlite3
│  manage.py
│
├─.idea
│  │  .gitignore
│  │  misc.xml
│  │  modules.xml
│  │  mysite1.iml
│  │  vcs.xml
│  │  workspace.xml
│  │
│  └─inspectionProfiles
│          profiles_settings.xml
│          Project_Default.xml
│
├─mysite1
│  │  asgi.py
│  │  settings.py	# 项目的配置文件--包含项目启动时需要的配置
│  │  urls.py		# 项目主路由配置--HTTP请求进入Django时，优先调用该文件
│  │  wsgi.py		# web服务网关的配置文件--Django正式启动时，需要用到
│  │  __init__.py	# Python包的初始化文件
│  │
│  └─__pycache__
│          settings.cpython-38.pyc
│          urls.cpython-38.pyc
│          wsgi.cpython-38.pyc
│          __init__.cpython-38.pyc
│
└─templates

```

