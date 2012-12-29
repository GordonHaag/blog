from google.appengine.ext import db
import string

class GenericModel(db.Model):
	'''GenericModel is inherited by other model definitions.'''
	pass
class BlogEntry(GenericModel):
	title = db.StringProperty()
	markdown = db.TextProperty()
	html = db.TextProperty()
	last_updated = db.DateTimeProperty()
	author = db.UserProperty()
	visible = db.BooleanProperty()
	locator = db.StringProperty()
#	comments = db.ListProperty(db.Key)
	DateAdded = db.DateTimeProperty(auto_now_add = True)
	def summary(self, n=400):
		return self.html[:n]

	def make_locator(self):
		t = str(self.title.lower())
		ret=''
		for l in t:
			if l not in string.lowercase+string.digits:
				ret+='-'
			else:
				ret+=l
		if not self.locator:
			self.locator = ret
			self.put()
		return ret