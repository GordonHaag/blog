#!/usr/bin/env python
import webapp2
import models
import datetime
import jinja2, os # used for templating
from google.appengine.api import users
from google.appengine.ext import db
import markdown
import config
# open a jinja environment to allow jinja to function
j = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#Frontfacing handlers
class MainHandler(webapp2.RequestHandler):
    def get(self):
		entries = db.GqlQuery('''
			SELECT title, summary, locator FROM BlogEntry WHERE visible=True ORDER BY DateAdded DESC
			''').fetch(config.front_page_length)
		template = j.get_template('home.html')
		self.response.write(template.render({'entries':entries}))

class Archive(webapp2.RequestHandler):
    def get(self):
		entries = db.GqlQuery('''SELECT * FROM BlogEntry WHERE visible=True ORDER BY DateAdded DESC''')
		template = j.get_template('home.html')
		self.response.write(template.render({'entries':entries}))


class EntryHandler(webapp2.RequestHandler):
	def get(self, locator):
		template = j.get_template('entry.html')
		entry = db.GqlQuery('''SELECT * FROM BlogEntry WHERE locator = :1''', locator)[0]
		self.response.write(template.render({'entry':entry}))
		#self.response.write(locator+',' + entry.locator)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (r'/entry/(\S+)', EntryHandler),
    ('/arc', Archive),
		], debug=True)