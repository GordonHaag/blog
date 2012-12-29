#!/usr/bin/env python
import webapp2
import models
import datetime
import jinja2 # used for templating
import os # used by jinja2 
from google.appengine.api import users
from google.appengine.ext import db

# open a jinja environment to allow jinja to function
j = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
		template = j.get_template('home.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
