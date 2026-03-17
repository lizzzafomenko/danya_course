## Task 2

В общем все по заданию.

### [`gttp_server.py`](./gttp_server.py)
### [`gttp_client.py`](./gttp_client.py)
### [`gttp_async_server.py`](./gttp_async_server.py)

**Входные параметры:**
*   `--ip` (`-ip`): IP
*   `--port` (`-p`): server port

```
python gttp_server.py --ip 127.0.0.1 --port 12345
python gttp_client.py --ip 127.0.0.1 --port 12345

python gttp_async_server.py --ip 127.0.0.1 --port 12345
```

Единственное что не добавила timeout на сервер, потому что как-то странно, если клиент будет думать "какое бы число мне написать" а сервер раз в 5 секунд будет ему спамить.

Но на клиента добавила timeout, задаем с `HELO 5.0`. 


#### **timeout работает**

Чтобы проверить и показать, что оно работает, смотри скрин ниже (поставила server.sleep перед ответом клиенту)

<img src="screens/artificial_timeout.png" width="600" height="400">

#### **а бывает такое, что timepout действительно происходит (без sleep)**

<img src="screens/real_timeout.png" width="600" height="400">

#### **пример выигрыша**

<img src="screens/winner.png" width="600" height="400">

#### **пример проигрыша**

<img src="screens/looser.png" width="600" height="400">