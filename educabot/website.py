#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cherrypy

class SimpleWebsite(object):
    @cherrypy.expose
    def index(self):
        return "<h1>EducaBot is running...</h1>"