from tornado import ioloop
import tornado
from tornado import httpserver
from application import Application
import config

if __name__ == '__main__':
    app = Application()
    httpServer =httpserver.HTTPServer(app)
    httpServer.bind(config.option['port'])
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()
    print('run in 127.0.0.1:9999...')