#!/usr/bin/env python
import webapp2
import models
import datetime
import jinja2 # used for templating
import os # used by jinja2 
from google.appengine.api import users
from google.appengine.ext import db
import markdown

# open a jinja environment to allow jinja to function
j = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#Frontfacing handlers
class MainHandler(webapp2.RequestHandler):
    def get(self):
		entries = db.GqlQuery('''SELECT * FROM BlogEntry WHERE visible=True ORDER BY DateAdded DESC LIMIT 7''')
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

#Admin handlers
class Admin(webapp2.RequestHandler):
	def get(self):
		template = j.get_template('admin.html')
		self.response.write(template.render())

class EntryView(webapp2.RequestHandler):
	def get(self, key=None):
		if key: #editing
			entry = db.get(key)
			template = j.get_template('edit.html')
		else:
			entry = models.BlogEntry()
			template = j.get_template('add.html')
		self.response.write(template.render({'obj':entry}))

	def post(self, key=None):
		if key: # editing
			new = db.get(key)
		else: # adding
			new = models.BlogEntry()	
		new.title = self.request.get('title')
		new.markdown = self.request.get('content')
		new.html = markdown.markdown(self.request.get('content'), output_format='html5')
		new.last_updated = datetime.datetime.now()
		new.author = users.get_current_user()
		new.locator = new.make_locator()
		if self.request.get('draft') == 'yes':
			new.visible = False
		else:
			new.visible = True
		new.put()
		#self.response.write(str(str(new.key())==str(key)))

		self.redirect('/admin/')

class AdminList(webapp2.RequestHandler):
	def get(self):
		template = j.get_template('list.html')
		entries = db.GqlQuery('''
			SELECT * FROM BlogEntry ORDER BY last_updated DESC''')
		self.response.write(template.render({'entries':entries}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (r'/entry/(\S+)', EntryHandler),
    ('/arc', Archive),
    ('/admin', AdminList),
	('/admin/', AdminList),
    ('/admin/add', EntryView),
    ('/admin/list', AdminList),
    (r'/admin/edit/(\S+)', EntryView),
		], debug=True)
