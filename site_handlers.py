#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import datetime
from models import Uporabnik, Sporocilo
from secret import secret
import time
import hmac
import hashlib

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


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

        cookie_value = self.request.cookies.get('uid')

        if cookie_value:
            params['logiran'] = self.preveri_cookie(cookie_vrednost=cookie_value)
        else:
            params['logiran'] = False

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def ustvari_cookie(self, uporabnik):
        uporabnik_id = uporabnik.key.id()
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=10)
        expires_ts = int(time.mktime(expires.timetuple()))
        sifra = hmac.new(str(uporabnik_id), str(secret) + str(expires_ts), hashlib.sha1).hexdigest()
        vrednost = "{0}:{1}:{2}".format(uporabnik_id, sifra, expires_ts)
        return  self.response.set_cookie(key='uid', value=vrednost, expires=expires)

    def preveri_cookie(self, cookie_vrednost):
        uporabnik_id, sifra, expires_ts = cookie_vrednost.split(':')

        if datetime.datetime.utcfromtimestamp(float(expires_ts)) > datetime.datetime.now():
            preverba = hmac.new(str(uporabnik_id), str(secret) + str(expires_ts), hashlib.sha1).hexdigest()

            if sifra == preverba:
                return True
            else:
                return False


class MainHandler(BaseHandler):
    def get(self):
        datum = datetime.datetime.now()
        danes = datetime.datetime.strftime(datum,"%d.%m.%Y")
        tocen_cas = datum + datetime.timedelta(hours=1)
        cas = datetime.datetime.strftime(tocen_cas, "%H:%M:%S")
        params = {'datum':danes,"cas":cas}
        return self.render_template("index.html",params=params)

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
        return self.render_template("contact.html")

    def post(self):
        sporocilo = self.request.get('sporocilo')

        sporocilo = Sporocilo(sporocilo=sporocilo)
        potrditev = "Hvala za tvoje sporocilo :)"
        sporocilo.put()
        params = {'potrditev':potrditev}
        return self.render_template('contact.html', params=params)




# kontroler za  zavihek projekti
class ProjectsHandler(BaseHandler):
    def get(self):
        return self.render_template("projects.html")

# kontroler registracija novega uporabnika
class RegistracijaHandler(BaseHandler):
    def get(self):
        return self.render_template('registracija.html')

    def post(self):
        ime = self.request.get('ime')
        priimek = self.request.get('priimek')
        email = self.request.get('email')
        geslo = self.request.get('geslo')
        ponovno_geslo = self.request.get('ponovno_geslo')

        mail_obstaja  = Uporabnik.query(Uporabnik.email == email).fetch()

        if mail_obstaja:
           return self.write('email je ze v bazi')

        elif geslo == ponovno_geslo:
            Uporabnik.ustvari(ime=ime, priimek=priimek, email=email, original_geslo=geslo)
            return self.redirect_to('login')
        else:
            return self.write('Gesli se ne ujemata')


# kontroler za  prijavo uporabnikov
class LoginHndler(BaseHandler):
     def get(self):
         return self.render_template('login.html')

     def post(self):
         try:
             email = self.request.get('email')
             geslo = self.request.get('geslo')
             uporabnik = Uporabnik.query(Uporabnik.email == email).get()
             if Uporabnik.preveri_geslo(original_geslo=geslo, uporabnik=uporabnik):
                self.ustvari_cookie(uporabnik=uporabnik)
                return self.redirect('/contact')
             else:
                 return self.write('Prišlo je do napake mail ali geslo ni pravilno ce se nisi se Registriraj :(')
         except:
             return self.write('Prislo je do Napke Pred prvo prijavo je obvezna registracija Pazi na pravilen podatkov')
