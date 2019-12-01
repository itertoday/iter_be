
from websocket import create_connection
import json


WS_URL = "ws://localhost:8888/ws"  


class NotificationClient(object):

    def __init__(self, url=WS_URL):
        self.url = url
        self._ws = None
        self._init()

    @property
    def websocket(self):
        return self._ws

    def _init(self):
        self._ws = create_connection(self.url)

    def __enter__(self):
        return self.websocket

    def __exit__(self, exec_type, exec_trace, exec_value):
        self.websocket.close()

if __name__ == "__main__":
    with NotificationClient() as client:
        payload = dict(action="orderHandler", tracker="3289-HJAHASJ-20192812")
        message = json.dumps(payload)
        client.send(message)
        result =  client.recv()
        print(result)
    print("closed!")



