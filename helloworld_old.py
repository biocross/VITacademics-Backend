#updated on 11/10/2012 - "SLot" on "last updated" issue fix.

import _mechanize
import webapp2, cookielib
from _mechanize import Browser
from BeautifulSoup import BeautifulSoup
from google.appengine.ext import db


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('VITattendace Scraping Base \nRunning On The Google App Engine. \nLast Update: 30 July 2012 \n\n(c) 2012 Siddharth Gupta (B.Tech ECE - VIT)')

class DetailsExtractor(webapp2.RequestHandler):
	def get(self, regno, dob, subject):
		self.response.headers['Content-Type'] = 'text/html'
		br= _mechanize.Browser()
		cj = cookielib.LWPCookieJar()
		br.set_cookiejar(cj)
		br.set_handle_equiv(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		n=262
		while(n<=262):
			m=str(n).zfill(4) # filling zeros for roll no like 001,002 etc.
			n=n+1
			#self.response.write('11BEC') # This is where roll no goes, for 09BCE just replace by 09BCE.
			u=regno
			r=br.open('https://academics.vit.ac.in/parent/parent_login.asp')
			html=r.read()
			soup=BeautifulSoup(html)
			final=""
			e = soup("img")
			decider = len(e)
			if (decider==5):
				op="*"
			else:
				op = "+"
			for i in range(1, len(e), 1):
				z= str(e[i]).split("/")
				y= str(z[1]).split(".png")
				if (len(y[0])==1):
					final=final+y[0]
				else :
					final=final+op
			captcha=str(eval(final)) #final captcha
			br.select_form('parent_login')
			br.form['wdregno']=u
			br.form['vrfcd']=str(captcha)
			br.form['wdpswd'] = dob
			response=br.submit()
			resp = br.open('https://academics.vit.ac.in/parent/attn_report.asp?sem=FS')
			l = int(subject)
			br.select_form(nr=l)
			response2 = br.submit()
			details = BeautifulSoup(response2)
			last = details("td")
			self.response.write(last[len(last)-5].text)


class Extractor(webapp2.RequestHandler):
	def get(self, regno, dob):
		self.response.headers['Content-Type'] = 'text/html'
		br= _mechanize.Browser()
		cj = cookielib.LWPCookieJar()
		br.set_cookiejar(cj)
		br.set_handle_equiv(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		n=262
		while(n<=262):
			m=str(n).zfill(4) # filling zeros for roll no like 001,002 etc.
			n=n+1
			#self.response.write('11BEC') # This is where roll no goes, for 09BCE just replace by 09BCE.
			u=regno
			r=br.open('https://academics.vit.ac.in/parent/parent_login.asp')
			html=r.read()
			soup=BeautifulSoup(html)
			final=""
			e = soup("img")
			decider = len(e)
			if (decider==5):
				op="*"
			else:
				op = "+"
			for i in range(1, len(e), 1):
				z= str(e[i]).split("/")
				y= str(z[1]).split(".png")
				if (len(y[0])==1):
					final=final+y[0]
				else :
					final=final+op
			captcha=str(eval(final)) #final captcha
			br.select_form('parent_login')
			br.form['wdregno']=u
			br.form['vrfcd']=str(captcha)
			br.form['wdpswd'] = dob
			response=br.submit()
			resp = br.open('https://academics.vit.ac.in/parent/attn_report.asp?sem=FS')
			page=resp.read()
			soup=BeautifulSoup(page)
			tr=soup('td') # taking all the tr tags
			length = len(tr) -3
			self.response.write("<table>")
			#self.response.write("<tr id=\"content\">")
			for i in range(16, length, 1):
				if tr[i].text == "-":
					self.response.write("<tr>Not Uploaded</tr>")
				elif tr[i].text == "":
					self.response.write("<tr>Not Available</tr>")
				else:
					self.response.write("<tr>" + tr[i].text + "</tr>")
			self.response.write("</table>")
			
			users = db.Query(User)
			users.filter("number = ", u)
			try:
				if (users.get() != None):
					print ""
				else:
					cur = User(number = str(regno), dob = str(dob))
					cur.put()
					print ""
			except:
				print ""

			
			
		
class User(db.Model):
	number = db.StringProperty()
	dob = db.StringProperty()		
		
		
class About(webapp2.RequestHandler):
	def get(self):
		self.response.write("Created by: <br/> Siddharth Gupta")
		



app = webapp2.WSGIApplication([('/', MainPage), ('/att/(.*)/(.*)', Extractor), ('/about', MainPage), ('/det/(.*)/(.*)/(.*)', DetailsExtractor)],
                              debug=True)