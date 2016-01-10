#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import datetime
from models import Sporocilo, User
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import urlfetch
import json
from secret import secret
import time
import hmac
import hashlib

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

# testni komentar
class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
# spremenljivka cooki_value dobi vrednost ko je uporabnik logiran
        cookie_value = self.request.cookies.get('uid')

# ce je uporabnik logiran torej obstaja veljaven piskot se v paremtre doda logiran
# v nasprotnem primeru velja da uporabnik ni logiran
        if cookie_value:
            params['logiran'] = self.preveri_cookie(cookie_vrednost=cookie_value)
        else:
            params['logiran'] = False

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def trenutni_datum_cas(self):
        now = datetime.datetime.now()
        slo_datum = now + datetime.timedelta(hours=1)
        danes = datetime.datetime.strftime(slo_datum, '%d.%m.%Y %H:%M:%S')
        datum = datetime.datetime.strptime(danes, '%d.%m.%Y %H:%M:%S')
        return datum


# funkcija ustvari cookie v katerega se zapise id uporabnik ki je trenutno prijavljen
    def ustvari_cookie(self, uporabnik):
        uporabnik_id = uporabnik.key.id()
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=10)
        expires_ts = int(time.mktime(expires.timetuple()))
        sifra = hmac.new(str(uporabnik_id), str(secret) + str(expires_ts), hashlib.sha1).hexdigest()
        vrednost = "{0}:{1}:{2}".format(uporabnik_id, sifra, expires_ts)
        return  self.response.set_cookie(key='uid', value=vrednost, expires=expires)

# funkcija preveri veljanost cookie - nastavljeno velja 10 dni
    def preveri_cookie(self, cookie_vrednost):
        uporabnik_id, sifra, expires_ts = cookie_vrednost.split(':')

        if datetime.datetime.utcfromtimestamp(float(expires_ts)) > datetime.datetime.now():
            preverba = hmac.new(str(uporabnik_id), str(secret) + str(expires_ts), hashlib.sha1).hexdigest()

            if sifra == preverba:
                return True
            else:
                return False

 # ------- Kontrolerji za glavno ravne strani ------

# kontroler za osnovno stran index.html

class MainHandler(BaseHandler):
    def get(self):
        datum = datetime.datetime.now()
        danes = datetime.datetime.strftime(datum,"%d.%m.%Y")
        tocen_cas = datum + datetime.timedelta(hours=1)
        cas = datetime.datetime.strftime(tocen_cas, "%H:%M:%S")


        # vreme api open weather map :)
        url = "http://api.openweathermap.org/data/2.5/weather?q=Cerkno,uk&units=metric&appid=425d08d39ad4a87c17bcb351795ba4c3"
        result = urlfetch.fetch(url)
        podatki = json.loads(result.content)
        params = {'datum':danes,"cas":cas, 'podatki': podatki}

        return self.render_template("index.html",params=params)


# Prijava uporabnika  za dostop do aplikacij kjer je  prijava potrebna
# osnovna prijavna stran

class PrijavaHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()

        if uporabnik:
            prijavljen = True
            logout_url = users.create_logout_url('/')
            params = {'uporabnik': uporabnik, 'prijavljen':prijavljen, 'logout_url':logout_url}
            return self.render_template('prijavi_se.html', params=params)
        else:
            prijavljen = False
            login_url = users.create_login_url('/prijavi-se')
            params = {'prijavljen': prijavljen, 'login_url': login_url}
            return self.render_template('prijavi_se.html', params=params)

class PozdravUporabnikHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            params = {'uporabnik': uporabnik}
            return self.render_template('preveri_mail.html', params=params)
        else:
            self.redirect_to('prijava')

    def post(self):
        uporabnik = users.get_current_user()
        email = uporabnik.email()
        reg_uporabnik = User.query(User.email == email).fetch()

        if reg_uporabnik:
            return self.redirect_to('main')
        else:
            # redirect_to reg-uporabnika
            return self.redirect_to('reg-uporabnika')

class RegUporabnikaHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        params = {'uporabnik': uporabnik}
        return self.render_template('reg_uporabnika.html', params=params)

    def post(self):
        uporabnik = users.get_current_user()
        ime = self.request.get('ime')
        priimek = self.request.get('priimek')
        vzdevek = uporabnik.nickname()
        email = uporabnik.email()
        regisriran = True

        nov_uporabnik = User(ime=ime, priimek=priimek, vzdevek=vzdevek, email=email, regisriran=regisriran)
        nov_uporabnik.put()

        return self.redirect_to('main')



# Kontroler za zavihek  o meni
class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")

# kontroler Blog
class BlogHandler(BaseHandler):
    def get(self):
        return self.render_template("blog.html")

# kontroler Aktivnosti
class ActivitiesHandler(BaseHandler):
    def get(self):
        return self.render_template("activities.html")

# Kontroler kontakt
class ContactHandler(BaseHandler):
    def get(self):
        uporabnik = users.get_current_user()
        if uporabnik:
            params = {'uporabnik': uporabnik}
            return self.render_template("contact.html", params=params)
        else:
            return self.render_template('contact.html')


    def post(self):
        uporabnik = users.get_current_user()
        vzdevek = uporabnik.nickname()
        email = uporabnik.email()
        msg = self.request.get('sporocilo')
        danes = datetime.datetime.now()
        datum = self.trenutni_datum_cas()
        sporocilo = Sporocilo(sporocilo=msg, vzdevek=vzdevek, email=email, nastanek=datum)
        potrditev = "Hvala za tvoje sporocilo :)"
        sporocilo.put()

        # sporocila iz kontaktnega obrazca dobim na mail
        e_posta = mail.EmailMessage(sender=email,
                                    to='janko.pirih@gmail.com',
                                    subject="Kontakt sporocilo iz domace strani od %s" % vzdevek,
                                    body=msg)
        e_posta.send()

        params = {'potrditev':potrditev, 'uporabnik':uporabnik}
        return self.render_template('contact.html', params=params)

# kontroler za  zavihek projekti
class ProjectsHandler(BaseHandler):
    def get(self):
        return self.render_template("projects.html")


