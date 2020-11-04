# 性能对比

## 延时API

 `slowapi/api.py`

``` PYTHON
import os
import asyncio
from aiohttp import web

async def handle(request):
    delay = float(request.query.get('delay') or 1)
    await asyncio.sleep(delay)
    text = '延时时间:{}秒'.format(delay)
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, port=5200)
```

启动 `python api.py`

ab 并发量2000 客户端数量200

``` shell
ab -r -n 2000 -c 200 http://127.0.0.1:5000/?delay=1
```

## 服务端代码

 `app/__init__.py`

``` python
from flask import Flask,request
import time
import requests

app = Flask(__name__)

@app.route('/')
def index():
    delay = float(request.args.get('delay') or 1)

    url = 'http://127.0.0.1:5200/?delay={}'.format(delay)

    resp = requests.get(url)
    return 'Hi there! ' + resp.text
```

## 单独gevent  wsgi启动

 `pywsgi.py`

``` python
from gevent import monkey
monkey.patch_all()

import os
from gevent.pywsgi import WSGIServer
from app import app

http_server = WSGIServer(('',5000), app)
http_server.serve_forever()
```

 `python pywsgi.py`

## 单独Flask启动

 `run.py`

``` python
from app import app
```

``` shell
export FLASK_APP=run.py
flask run
```

## Gunicorn启动

``` shell
gunicorn app:app -b 0.0.0.0:5000 -w 4

```

## Gunicorn + gevent

 `patched.py`

``` python
from gevent import monkey
monkey.patch_all()

from app import app
```

``` python
gunicorn patched:app -b 0.0.0.0:5000 -w 4 -k gevent
```

## 结果

|                   | 并发用户数 | 花费时间(秒) | 请求数量 | 失败 | 转让总额(bytes)： | 传送的HTML( bytes) | 吞吐率(每秒) | 用户请求等待时间(毫秒) | 服务器请求等待时间(毫秒) | 传输速率(K/S) |
| ----------------- | ---------- | ------------ | -------- | ---- | ----------------- | ------------------ | ------------ | ---------------------- | ------------------------ | ------------- |
| python single.py  | 200        | 12.513       | 2000     | 0    | 364000            | 58000              | 159.84       | 1251.273               | 6.256                    | 28.41         |
| flask run         | 200        | 11.354       | 2000     | 0    | 364000            | 58000              | 176.15       | 1135.395               | 5.677                    | 31.31         |
| gevent            | 200        | 15.221       | 2000     | 0    | 328000            | 58000              | 131.39       | 1522.144               | 7.611                    | 21.04         |
| Gunicorn          | 200        | 24.278       | 2000     | 96   | 18144             | 2784               | 82.38        | 2427.829               | 12.139                   | 0.73          |
| Gunicorn + GEVENT | 200        | 11.05        | 2000     | 0    | 378000            | 58000              | 180.99       | 1105.042               | 5.525                    | 33.41         |
