import tornado.ioloop
import tornado.web
import uuid
from tornado import websocket
import json
clients = []

PORT = 8888

class IterMessageOrderHandler(object):
    def __init__(self, socket, payload):
        self._socket = socket
        self._payload = payload

    @property
    def socket(self):
        return self._socket

    @property
    def payload(self):
        return self._payload

    def execute(self):
        print('executing with payload')
        output = {
            'message': 'Order # {} was Accepted! Details:'.format(self.payload['pk']),
            'trackerID': self.payload['fields']['tracker'],
            'id': self.socket.uuid #Add details of transporter
        }
        for client in clients:
            print("Send to tracker: ", client.uuid)
            client.write_message(json.dumps(output))

class IterMessageHandler(object):

    handlers = {
        'orderHandler': IterMessageOrderHandler
    }

    @classmethod
    def execute(cls, socket, payload):
        action = payload['action']
        clazz = cls.handlers[action]
        clazz(socket, payload).execute()


class NotificationWebSocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        self.uuid = str(uuid.uuid4())
        clients.append(self)
        print("WebSocket opened: ", len(clients))

    def on_message(self, message):
        payload = json.loads(message)
        print("on_message", payload)
        IterMessageHandler.execute(self, payload)
        
            
    def on_close(self):
        client = next(c for c in clients if c.uuid == self.uuid)
        print("found", client)
        clients.remove(client)
        print("WebSocket closed")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/ws", NotificationWebSocketHandler),
    ])
    application.listen(PORT)
    tornado.ioloop.IOLoop.current().start()