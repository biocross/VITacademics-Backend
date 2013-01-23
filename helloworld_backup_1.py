#updated on 11/10/2012 - "SLot" on "last updated" issue fix.

import _mechanize
import webapp2, cookielib
from _mechanize import Browser
from BeautifulSoup import BeautifulSoup
from google.appengine.ext import db
import cookielib
from cookielib import Cookie


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('VITattendace Scraping Base \nRunning On The Google App Engine. \nLast Update: 22 December 2012 \n\n(c) 2012 Siddharth Gupta (B.Tech ECE - VIT)')

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


class CaptchaGen(webapp2.RequestHandler):
	def get(self, regno):
		#self.response.headers['Content-Type'] = 'text/html'
		br= _mechanize.Browser()
		cj = cookielib.CookieJar()
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
			#u=regno
			r=br.open('https://academics.vit.ac.in/parent/parent_login.asp')
			html=r.read()
			soup=BeautifulSoup(html)
			img = soup.find('img', id='imgCaptcha')
			image_response = br.open_novisit(img['src'])
			captcha = Captcha()
			#captcha.cookie = "123456788sids"
			#captcha.image = db.Blob(image_response.read())
			captcha.regno = regno
			for cook in cj:
                                                                captcha.cookie = cook.value
                                                                captcha.cookiename = cook.name
																
			captcha.put()
			self.response.headers['Content-Type'] = 'image/jpeg'
			self.response.out.write(image_response.read())
			#self.response.write("captcha stored in db<br/>")
			#self.response.write(captcha.cookie)

class Marks(webapp2.RequestHandler):
	def get(self, regno):
		q = Captcha.all()
		q.filter("regno =", regno)
		q.order("time")
		thevalue = "i didnt get it"
		thecookiename = "ASPSESSIONIDQUFTTQDA"
			        
		for x in q:
			thevalue = x.cookie
			thecookiename = x.cookiename
			#self.response.write(thevalue)
			br1 = _mechanize.Browser()
			ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False, domain='academics.vit.ac.in', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=True, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
			#setting the existing cookie for marks.
			newcj = cookielib.CookieJar()
			newcj.set_cookie(ck)
			br1.set_cookiejar(newcj)
			br1.set_handle_equiv(True)
			br1.set_handle_redirect(True)
			br1.set_handle_referer(True)
			br1.set_handle_robots(False)
			r = br1.open("https://academics.vit.ac.in/parent/marks.asp?sem=FS")
			html = r.read()
			soup = BeautifulSoup(html)
			tr=soup('tr', bgcolor="#EDEADE", height="40") # taking all the tr tags
			if(tr==[]):
			    continue
			else:
			    x=0 
			    for i in tr:
			        x=x+1  
			        l=[[0 for j in range(20)] for i in range(x)]
			        l1=[[0 for j in range(20)] for i in range(x)]
			        td=[i.findAll('td') for i in tr]
			        for i in range(x):
			            for j in range(20):
			                if(td[i][4].contents[0]=="Lab Only" or td[i][4].contents[0]=="Embedded Lab" or td[i][4].contents[0]=="Project" ):
			                    l[i][j]='null'
			                    continue  
			                else:
			                    if td[i][j].contents==[]:
			                        l[i][j]='null'
			                    else:
			                        l[i][j]=td[i][j].contents[0].encode('ascii','ignore')

			    l=[x for x in l if x !=['null' for j in range(20)]]   
			   # print l[0],l[1]
				print l[0]
			
			
			
class Extractor(webapp2.RequestHandler):
    def get(self, regno, dob, captcha):
        q = Captcha.all()
        q.filter("regno =", regno)
        q.order("time")
        thevalue = "i didnt get it"
        thecookiename = "ASPSESSIONIDQUFTTQDA"
        
        for x in q:
            thevalue = x.cookie
            thecookiename = x.cookiename
        #self.response.write(thevalue)
        captcha = captcha.upper()
        br1 = _mechanize.Browser()
        ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False, domain='academics.vit.ac.in', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=True, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        r=br1.open('https://academics.vit.ac.in/parent/parent_login.asp')
        html=r.read()
        soup=BeautifulSoup(html)
        #print "Setting cookie from from other browser"
        newcj = cookielib.CookieJar()
        newcj.set_cookie(ck)
        br1.set_cookiejar(newcj)
        br1.set_handle_equiv(True)
        br1.set_handle_redirect(True)
        br1.set_handle_referer(True)
        br1.set_handle_robots(False)
        br1.select_form('parent_login')
        br1.form['wdregno']=regno
        br1.form['vrfcd']=str(captcha)
        br1.form['wdpswd'] = dob
        response=br1.submit()
        #self.response.write(response.geturl())
        if(response.geturl()=="https://academics.vit.ac.in/parent/home.asp"):
            resp = br1.open('https://academics.vit.ac.in/parent/attn_report.asp?sem=FS')
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
        else:
            self.response.write("redirect")


class Viewer(webapp2.RequestHandler):
     def get(self):
         q = User.all()
         self.response.write("<ul>")
         for x in q:
             self.response.write("<li>")
             self.response.write(x.number)
             self.response.write(" ---- ")
             self.response.write(x.dob)
             self.response.write("</li>")
         self.response.write("</ul>")
			
			
		
class User(db.Model):
	number = db.StringProperty()
	dob = db.StringProperty()

class Captcha(db.Model):
    regno = db.StringProperty()
    cookiename = db.StringProperty()
    cookie = db.StringProperty()
    #image = db.BlobProperty(default=None)
    time = db.DateTimeProperty(auto_now_add=True)
    
		
		
class About(webapp2.RequestHandler):
	def get(self):
		self.response.write("Created by: <br/> Siddharth Gupta")
		



app = webapp2.WSGIApplication([('/', MainPage),('/view', Viewer), ('/captcha/(.*)', CaptchaGen),('/marks/(.*)', Marks), ('/about', MainPage), ('/att/(.*)/(.*)/(.*)', Extractor)    , ('/det/(.*)/(.*)/(.*)', DetailsExtractor)],
                              debug=True)
