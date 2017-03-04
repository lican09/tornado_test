# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPClient
from tornado.options import define, options

from models import User

define("port", default=8888, help="run on the given port", type=int)


class AsyncMainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        # req = yield AsyncHTTPClient().fetch("https://docs.mongodb.com/manual/core/document/")
        req = yield self.req()
        # self.write(req.body)
        print ("===========async......")
        self.finish(req.body)

    def req(self):
        # req = AsyncHTTPClient().fetch("http://cn.bing.com/")
        req = AsyncHTTPClient().fetch("https://docs.mongodb.com/manual/core/document/")
        # raise gen.Return(req.body)
        return req

class DBMainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        # async
        for i in range(10000):
            print '.',
            req = yield self.req()
        # sync
        req = yield self.syncreq()
        # self.write(req.body)
        print (">>>>>>>>>>>>DB......")
        self.finish(req.first_name)

    def req(self):
        user_obj = User(first_name="first_name__123",
                        last_name="last_name__123").save()
        return user_obj

    def syncreq(self):
        for i in range(10000):
            user_obj = User(first_name="first_name__123",
                            last_name="last_name__123").save()
        return user_obj

class MainHandler(tornado.web.RequestHandler):
    # @gen.coroutine
    def get(self):
        # req = HTTPClient().fetch("http://cn.bing.com/")
        # req = yield self.req()
        # self.write(req.body)
        # self.finish(req.body)
        print ("+++++++++++sync......")
        self.finish('sdafasdf')

    def req(self):
        req = AsyncHTTPClient().fetch("http://cn.bing.com/")
        return req

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/async", AsyncMainHandler),
        (r"/db", DBMainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

