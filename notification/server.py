import tornado.ioloop
import tornado.web

from tornado import websocket

class NotificationWebSocketHnadler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/ws", NotificationWebSocketHnadler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()