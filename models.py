#!/usr/bin/env python
# encoding: utf-8

import tornado.ioloop
from motorengine.connection import connect
from motorengine import Document, StringField


io_loop = tornado.ioloop.IOLoop.instance()
connect("tornado_test", host="localhost", port=27017, io_loop=io_loop)

class User(Document):
    __collection__ = "users"  # optional. if no collection is specified, class name is used.

    first_name = StringField(required=True)
    last_name = StringField(required=True)

    @property
    def full_name(self):
        return "%s, %s" % (self.last_name, self.first_name)
